# AI Copilot Backend (FastAPI)

FastAPI backend that exposes chat and health endpoints, integrating with Google's Gemini API to generate assistant replies.

## Quickstart

1) Install dependencies (Python 3.10+ recommended)
   - Create and activate a virtual environment (optional but recommended)
     - python -m venv .venv
     - source .venv/bin/activate  (Windows: .venv\Scripts\activate)
   - pip install -r requirements.txt

2) Environment variables
   - Copy .env.example to .env
     - cp .env.example .env
   - Edit .env and set:
     - GEMINI_API_KEY=YOUR_KEY_HERE
     - GEMINI_MODEL=gemini-1.5-flash (default is fine)
     - ALLOWED_ORIGINS=http://localhost:3000 (for local React dev)
   Notes:
   - Do not commit real keys.
   - ALLOWED_ORIGINS can be a comma-separated list or "*" for permissive CORS.

3) Run the server (port 3001)
   - uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload

4) Explore API
   - OpenAPI docs: http://localhost:3001/docs
   - OpenAPI JSON: http://localhost:3001/openapi.json

## Endpoints

- GET /health
  - Returns {"status": "ok"} if the service is healthy.

- POST /chat
  - Body: { "message": string, "history": [{ "role": "user"|"assistant", "content": string }] }
  - Response: { "reply": string }

## CORS

CORS is configured via the ALLOWED_ORIGINS environment variable.
- For local development with the React app, set: ALLOWED_ORIGINS=http://localhost:3000
- You can also specify multiple origins as a comma-separated list, e.g.:
  ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com
- Setting "*" will allow all origins (use with caution).

## Regenerate OpenAPI JSON

This repository includes a small script to regenerate the OpenAPI spec file for distribution:
- python -m src.api.generate_openapi

It writes the latest schema to interfaces/openapi.json. Ensure the app imports succeed (env variables can remain unset for schema generation).
