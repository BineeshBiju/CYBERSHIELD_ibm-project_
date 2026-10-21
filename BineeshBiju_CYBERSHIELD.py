#!/usr/bin/env python3
"""Serve the separate HTML/CSS frontend and the local audit API.

Run with: python web_app.py
The server listens on 127.0.0.1 only.
"""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from headers_cors_audit import audit

APP_DIR = Path(__file__).resolve().parent
MAX_REQUEST_BYTES = 16_384


class AuditRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        assets = {
            "/": ("index.html", "text/html; charset=utf-8"),
            "/index.html": ("index.html", "text/html; charset=utf-8"),
            "/style.css": ("style.css", "text/css; charset=utf-8"),
        }
        asset = assets.get(urlparse(self.path).path)
        if asset is None:
            self.send_error(404, "Not found")
            return

        filename, content_type = asset
        content = (APP_DIR / filename).read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(content)

    def do_POST(self):
        if urlparse(self.path).path != "/api/audit":
            self.send_error(404, "Not found")
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self._send_json(400, {"error": "Invalid Content-Length header."})
            return
        if content_length < 1 or content_length > MAX_REQUEST_BYTES:
            self._send_json(413, {"error": "Request body is empty or too large."})
            return

        try:
            payload = json.loads(self.rfile.read(content_length))
        except (json.JSONDecodeError, UnicodeDecodeError):
            self._send_json(400, {"error": "Request body must be valid JSON."})
            return

        if not isinstance(payload, dict) or payload.get("authorized") is not True:
            self._send_json(400, {"error": "Confirm that you are authorized to test this target."})
            return

        target = payload.get("url")
        if not isinstance(target, str):
            self._send_json(400, {"error": "Enter a valid HTTP or HTTPS URL."})
            return
        target = target.strip()
        if "://" not in target:
            target = "https://" + target
        parsed = urlparse(target)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname:
            self._send_json(400, {"error": "Enter a valid HTTP or HTTPS URL."})
            return

        self._send_json(200, audit(target, timeout=5))

    def _send_json(self, status, payload):
        content = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(content)

    def log_message(self, format_string, *args):
        print(f"{self.address_string()} - {format_string % args}")


def main():
    server = ThreadingHTTPServer(("127.0.0.1", 8765), AuditRequestHandler)
    print("CyberShield is available at http://127.0.0.1:8765")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping CyberShield.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
