# Company employee manager (FastAPI + Flask)

This repository contains a minimal example web app exposing two HTTP APIs for managing company employees:

- An async FastAPI app using Motor (async MongoDB driver)
- A sync Flask app using PyMongo

Both apps share models and connect to the same MongoDB database. See quick start below.

Environment

1) Create a `.env` file in the repo root with these values:

MONGODB_URI=mongodb://localhost:27017
DB_NAME=companydb

2) Create a virtual environment and install dependencies (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Run apps

- FastAPI (development):

```powershell
uvicorn app.fastapi_app.main:app --reload --port 8000
```

- Flask (development):

```powershell
# ensure .env or env vars are set, then
python -m app.flask_app.app
```

Notes

- Endpoints are simple CRUD for `employees` collection. FastAPI is async; Flask is sync.
- If you use a remote MongoDB (Atlas) update `MONGODB_URI` accordingly.
