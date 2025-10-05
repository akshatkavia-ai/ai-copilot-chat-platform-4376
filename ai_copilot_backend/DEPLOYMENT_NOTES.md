# Backend Deployment Notes

## Running the Backend Server

To ensure the backend accepts connections from external sources (including frontend preview environments), always start uvicorn with the following flags:

```bash
uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload
```

**Quick Start:** Use the provided startup script:
```bash
./start_server.sh
```

### Important Flags:
- `--host 0.0.0.0`: Binds to all network interfaces, allowing external connections (not just localhost)
- `--port 3001`: Backend runs on port 3001
- `--reload`: Auto-reloads on code changes (development only)

## CORS Configuration

The backend reads `ALLOWED_ORIGINS` from `.env`. This should include:
- `http://localhost:3000` (local React dev)
- `http://127.0.0.1:3000` (explicit IP)
- Any preview/production URLs for the frontend

## Environment Variables Required

Ensure `.env` contains:
```
GEMINI_API_KEY=<your-key>
GEMINI_MODEL=gemini-1.5-flash
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,<preview-url>
```

**Note:** Use `gemini-1.5-flash` as the default model. If you encounter 404 errors with `gemini-pro`, switch to `gemini-1.5-flash` which is the current stable model.

## Restart Instructions

After modifying `.env`:
1. Stop the backend process (Ctrl+C)
2. Restart with the uvicorn command above
3. Verify health: `curl http://127.0.0.1:3001/health`

After modifying frontend `.env`:
1. Stop the React dev server (Ctrl+C)
2. Run `npm start` again
3. Check browser console for any warnings about REACT_APP_API_BASE_URL

## Verification Steps

After starting the backend, verify it's running correctly:

1. Check if the process is listening on port 3001:
   ```bash
   lsof -i :3001
   ```
   Expected output should show uvicorn bound to `*:3001` (all interfaces)

2. Test the health endpoint:
   ```bash
   curl http://127.0.0.1:3001/health
   ```
   Expected response: `{"status":"ok"}`

3. Test with localhost:
   ```bash
   curl http://localhost:3001/health
   ```
   Should also return `{"status":"ok"}`

4. View API documentation:
   - Open browser to: http://localhost:3001/docs
   - Should display interactive Swagger UI

## Troubleshooting

### ERR_CONNECTION_REFUSED from Frontend

**Cause:** Backend not running or bound to wrong interface

**Solution:**
1. Verify backend is running: `lsof -i :3001`
2. If not running, start with: `./start_server.sh` or the uvicorn command
3. Ensure `--host 0.0.0.0` is used (not 127.0.0.1 or localhost)
4. Check ALLOWED_ORIGINS includes both `http://localhost:3000` and `http://127.0.0.1:3000`

### GEMINI_API_KEY Missing Error

**Cause:** .env file not configured or API key not set

**Solution:**
1. Copy `.env.example` to `.env`: `cp .env.example .env`
2. Edit `.env` and set your GEMINI_API_KEY
3. Restart the backend

### 404 or Model Not Found from Gemini API

**Cause:** Using deprecated or unavailable model (e.g., gemini-pro)

**Solution:**
1. Update GEMINI_MODEL in `.env` to: `gemini-1.5-flash`
2. Restart the backend

### CORS Errors in Browser Console

**Cause:** ALLOWED_ORIGINS doesn't include the frontend URL

**Solution:**
1. Update ALLOWED_ORIGINS in `.env` to include frontend URL
2. For local dev: `ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000`
3. Restart the backend
