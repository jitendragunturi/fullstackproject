import os
import json
from backend.app.db import init_db, get_db_path, get_kanban


def test_init_db_creates_file(tmp_path, monkeypatch):
    db_file = tmp_path / "test_pm.db"
    monkeypatch.setenv("DB_PATH", str(db_file))
    path = init_db()
    assert os.path.exists(path)


def test_get_kanban_returns_structure(tmp_path, monkeypatch):
    db_file = tmp_path / "test_pm2.db"
    monkeypatch.setenv("DB_PATH", str(db_file))
    init_db()
    board = get_kanban("user")
    assert "columns" in board
    assert "cards" in board
    assert isinstance(board["columns"], list)