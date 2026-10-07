# Polaris

Polaris is an open-source intelligence (OSINT) workbench for organizing research, source-backed results, and investigation cases.

## Current foundation

- FastAPI backend
- Health/readiness endpoints
- Environment-based configuration
- CORS configuration
- Render-ready deployment
- Test scaffold

## Local development

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate

pip install -r requirements.txt
uvicorn backend.main:app --reload
```

API:
- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/api/v1/health

## Production

The initial API is designed for deployment as a Render Web Service.

Build command:

```bash
pip install -r requirements.txt
```

Start command:

```bash
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

Secrets and provider credentials should be added through the deployment platform, never committed to Git.
