#!/bin/bash

# ── Absolute paths ─────────────────────────────────────────────────────────────
ROOT="$(cd "$(dirname "$0")" && pwd)"

# ── Kill all background processes on Ctrl+C ────────────────────────────────────
cleanup() {
    echo ""
    echo "🛑  Stopping servers..."
    kill 0
    exit 0
}
trap cleanup SIGINT SIGTERM

# ── Backend: FastAPI on :8000 ──────────────────────────────────────────────────
echo "🚀  Starting Backend  → http://localhost:8000"
cd "$ROOT/backend" && uv run uvicorn frontend_hoster:app --reload --port 8000 &

# ── Frontend: Vite on :5173 ────────────────────────────────────────────────────
echo "🚀  Starting Frontend → http://localhost:5173"
cd "$ROOT/frontend" && npm run dev --port 5173 &

# ── Done ───────────────────────────────────────────────────────────────────────
echo ""
echo "✅  Both servers running. Press Ctrl+C to stop."
echo "   Frontend → http://localhost:5173"
echo "   Backend  → http://localhost:8000"
echo ""
wait
