from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

from . import db
from . import routes

app = FastAPI()


@app.get("/api/health")
async def health():
    return {"status": "ok"}


# Include API routes
app.include_router(routes.router)


# Attempt to serve a built frontend if present at ../frontend/out
frontend_out = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend/out"))
if os.path.isdir(frontend_out):
    app.mount("/", StaticFiles(directory=frontend_out, html=True), name="frontend")
else:
    @app.get("/")
    async def root():
        return {"message": "Backend running. Build the frontend to serve static files."}


@app.on_event("startup")
def on_startup():
    # Initialize database on startup
    db_path = os.environ.get("DB_PATH")
    init_path = db.init_db(db_path) if db_path else db.init_db()
    print(f"Initialized DB at: {init_path}")
