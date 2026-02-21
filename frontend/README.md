# BiteWise Frontend

This is the React frontend for the BiteWise application. It is a beautiful, Discord-style UI that displays a grid of food tiles dynamically sourced from a backend server.

## Quick Start

To run the frontend development server, run the following command in your terminal from inside this `frontend` directory:

```bash
npm run dev
```

The application will start and be accessible in your browser at `http://localhost:5173/`.

### Prerequisites
Make sure you have Node.js and npm installed. Check by running `npm -v` and `node -v`.
Install the dependencies if you haven't already:
```bash
npm install
```

## Backend API Dependencies

This frontend relies on a backend running concurrently on `http://localhost:8000` to feed it data. Ensure the Python backend is running.

To start the backend, open a new terminal, navigate to the `backend` directory, and run:
```bash
cd ../backend
uv run uvicorn frontend_hoster:app --reload
```

**The frontend connects to the following backend endpoints:**

- `GET http://localhost:8000/api/recipes`
  - Fetches the list of all recipes with their `recipe_id`, `recipe_name`, and `url` to generate the card grid.

- `POST http://localhost:8000/api/select_recipe`
  - Sends a JSON payload containing the `user_id` and `recipe_id` when the user clicks the "Select" button on a specific recipe tile.
