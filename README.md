# AI-Powered Cloud Incident Response & Observability Platform

Status: Architecture approved (Step 1.1). Folder structure finalized (Step 1.2).
No application logic has been implemented yet.

See the approved architecture document for full design details, including
component responsibilities, data flow, the LangGraph workflow design, and
safety boundaries.

## Requirements

- **Python 3.11+** (see `.python-version`). Do not use Python 3.14 or another
  major version for this project.

## Environment Setup (Windows)

```powershell
# Create the virtual environment
py -3.11 -m venv .venv

# Activate it (PowerShell)
.venv\Scripts\Activate.ps1

# Activate it (Command Prompt, alternative)
.venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt
```

The `.venv/` directory is local to your machine and is excluded from
version control via `.gitignore`.
