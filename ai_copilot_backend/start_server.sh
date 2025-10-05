#!/bin/bash
# Startup script for AI Copilot Backend
# Ensures uvicorn binds to 0.0.0.0:3001 for external connectivity

cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "ERROR: .env file not found!"
    echo "Please copy .env.example to .env and configure your GEMINI_API_KEY"
    exit 1
fi

# Start uvicorn with correct binding
echo "Starting AI Copilot Backend on 0.0.0.0:3001..."
uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload
