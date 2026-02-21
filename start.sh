#!/bin/bash

# Define cleanup function to kill background processes on exit
cleanup() {
    echo "Stopping servers..."
    kill 0
    exit
}

# Trap termination signals to run the cleanup function
trap cleanup SIGINT SIGTERM

echo "Starting Backend (FastAPI)..."
cd backend
uv run uvicorn frontend_hoster:app --reload &
cd ..

echo "Starting Frontend (React/Vite)..."
cd frontend
npm run dev &
cd ..

echo "Both servers are running! Press Ctrl+C to stop them both."
wait
