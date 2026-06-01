# Backend AGENTS

This folder contains a minimal FastAPI backend scaffold for the Project Management MVP.

Files added:
- `app/main.py` — FastAPI app with `/api/health` and optional static serving of a built frontend.
- `requirements.txt` — Python dependencies (FastAPI, Uvicorn).

Next steps:
- Add database initialization and models in `app/db.py` and `app/models.py`.
- Add API routes for auth and Kanban CRUD in `app/routes.py`.
- Add AI client integration in `app/ai.py`.
This file should be updated with a description of the Backend