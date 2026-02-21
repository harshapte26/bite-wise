# ByteWise (Agent Hosting Platform)

Welcome to **ByteWise**, a full-stack AI Agent hosting solution.

This repository is structured as a monorepo containing both the React frontend and the Python Agent backend.

## Architecture

*   **`backend/`**: A Python-based API (using FastAPI and `uv` for dependency management) designed to host, manage, and execute AI agents. It handles memory, tools, streaming responses, and core agent logic.
*   **`frontend/`**: A React application (built with Vite) that provides the user interface for monitoring and interacting with the hosted AI agents.

## Getting Started

Follow these instructions to run the full application locally.

### Prerequisites

*   [Python 3.11+](https://www.python.org/downloads/)
*   [uv](https://docs.astral.sh/uv/) (Python package manager)
*   [Node.js](https://nodejs.org/) (for the React frontend)

---

### Running the Backend (Agent Host)

1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```
2. Sync dependencies and enter the virtual environment:
   ```bash
   uv sync
   ```
3. Run the development server (assuming a FastAPI or equivalent entry point in `src/main.py`):
   ```bash
   uv run src/main.py
   ```
   *(Note: You may need to use `uv run uvicorn src.main:app --reload` depending on your specific web framework setup.)*

---

### Running the Frontend (UI)

*We will initialize the frontend soon using Vite! Once initialized, follow these steps:*

1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the Vite development server:
   ```bash
   npm run dev
   ```

---

## Agent Structure

The backend is specifically designed for agent orchestration:

*   **`backend/src/agents/`**: Core definitions for autonomous agents.
*   **`backend/src/tools/`**: Actions the agents can perform (web search, DB queries, API calls).
*   **`backend/src/core/`**: Configuration and setup.
*   **`backend/src/api/`**: REST/WebSocket endpoints for the frontend to connect to the agents.
