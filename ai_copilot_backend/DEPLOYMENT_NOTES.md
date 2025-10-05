# Backend Deployment Notes

## Running the Backend Server

To ensure the backend accepts connections from external sources (including frontend preview environments), always start uvicorn with the following flags:

```bash
uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload
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
GEMINI_MODEL=gemini-pro
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,<preview-url>
```

## Restart Instructions

After modifying `.env`:
1. Stop the backend process (Ctrl+C)
2. Restart with the uvicorn command above
3. Verify health: `curl http://127.0.0.1:3001/health`

After modifying frontend `.env`:
1. Stop the React dev server (Ctrl+C)
2. Run `npm start` again
3. Check browser console for any warnings about REACT_APP_API_BASE_URL
