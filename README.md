# CyberShield

CyberShield is a small web application for reviewing HTTP security posture. It
checks security headers, cookies, and CORS behavior for a target you are
authorized to test. You can also load a saved JSON audit report and filter its
findings.

## Dataset

There is no bundled dataset. Live audits request the target URL and evaluate
its current HTTP responses; saved reports can be loaded as JSON.

For public web-measurement data and research, see the
[HTTP Archive](https://httparchive.org/). It is a separate public resource and
is not required or queried by this application.

## Technologies

- **Python 3** — local HTTP server and audit backend
- **HTML** — page structure and browser-side report rendering
- **CSS** — responsive dashboard styling
- **Requests** — HTTP requests used by the auditor

The server uses Python standard-library modules including `http.server`,
`json`, `pathlib`, and `urllib.parse`.

## Setup

1. Install Python 3.
2. From the project directory, create and activate a virtual environment
   (optional but recommended):

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install the Python dependency:

   ```powershell
   python -m pip install -r requirements.txt
   ```

## Run

The intended local server command is:

```powershell
python BineeshBiju_CYBERSHIELD.py
```

When the server starts successfully, open <http://127.0.0.1:8765/>. The server
is configured to listen on localhost.

**Current workspace note:** `BineeshBiju_CYBERSHIELD.py` imports
`headers_cors_audit`, but that module is not currently present in the project
directory. Restore the audit module alongside the server before running the
application. The command-line audit usage, when that module is available, is:

```powershell
python headers_cors_audit.py https://your-authorized-domain.example --json
```

## Using the dashboard

1. Enter an HTTP or HTTPS URL.
2. Confirm that you own the target or have permission to test it.
3. Start the audit and review the pass, warning, and failure findings.
4. Or choose a saved JSON report / paste JSON and select **Load report**.

Only scan targets that you own or are explicitly authorized to test.
