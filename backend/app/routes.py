from fastapi import APIRouter, HTTPException, Header
from typing import Optional
from . import db, models, ai
import sqlite3

router = APIRouter()


def _get_username_from_auth(authorization: Optional[str]) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    parts = authorization.split()
    if len(parts) == 2 and parts[0].lower() == "bearer":
        return parts[1]
    raise HTTPException(status_code=401, detail="Invalid Authorization header")


@router.post("/api/login")
async def login(req: models.LoginRequest):
    db_path = db.get_db_path()
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT password FROM users WHERE username=?", (req.username,))
    row = cur.fetchone()
    conn.close()
    if not row or row[0] != req.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    # For MVP, token is simply the username
    return {"token": req.username}


@router.get("/api/kanban")
async def get_kanban(authorization: Optional[str] = Header(None)):
    username = _get_username_from_auth(authorization)
    board = db.get_kanban(username)
    return board


@router.post("/api/kanban")
async def save_kanban_endpoint(board: dict, authorization: Optional[str] = Header(None)):
    username = _get_username_from_auth(authorization)
    # store whatever JSON payload frontend sends
    db.save_kanban(username, board)
    return {"status": "ok"}


@router.post("/api/ai/test")
async def ai_test(payload: dict, authorization: Optional[str] = Header(None)):
    username = _get_username_from_auth(authorization)
    prompt = payload.get("prompt", "2+2")
    resp = ai.call_ai(prompt, {})
    return resp
