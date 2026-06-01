import os
import sqlite3
import json


def get_db_path():
    return os.environ.get("DB_PATH", os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/pm.db")))


def init_db(db_path: str | None = None):
    db_path = db_path or get_db_path()
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS kanbans (username TEXT PRIMARY KEY, board_json TEXT)""")
    cur.execute("INSERT OR IGNORE INTO users(username,password) VALUES (?,?)", ("user", "password"))
    conn.commit()

    # Insert a sample kanban board for the default user if it doesn't exist
    cur.execute("SELECT board_json FROM kanbans WHERE username=?", ("user",))
    if not cur.fetchone():
        sample_board = {
            "columns": [
                {"id": "col-backlog", "title": "Backlog", "cardIds": ["card-1", "card-2"]},
                {"id": "col-discovery", "title": "Discovery", "cardIds": ["card-3"]},
                {"id": "col-progress", "title": "In Progress", "cardIds": ["card-4", "card-5"]},
                {"id": "col-review", "title": "Review", "cardIds": ["card-6"]},
                {"id": "col-done", "title": "Done", "cardIds": ["card-7", "card-8"]},
            ],
            "cards": {
                "card-1": {"id": "card-1", "title": "Align roadmap themes", "details": "Draft quarterly themes with impact statements and metrics."},
                "card-2": {"id": "card-2", "title": "Gather customer signals", "details": "Review support tags, sales notes, and churn feedback."},
                "card-3": {"id": "card-3", "title": "Prototype analytics view", "details": "Sketch initial dashboard layout and key drill-downs."},
                "card-4": {"id": "card-4", "title": "Refine status language", "details": "Standardize column labels and tone across the board."},
                "card-5": {"id": "card-5", "title": "Design card layout", "details": "Add hierarchy and spacing for scanning dense lists."},
                "card-6": {"id": "card-6", "title": "QA micro-interactions", "details": "Verify hover, focus, and loading states."},
                "card-7": {"id": "card-7", "title": "Ship marketing page", "details": "Final copy approved and asset pack delivered."},
                "card-8": {"id": "card-8", "title": "Close onboarding sprint", "details": "Document release notes and share internally."},
            },
        }
        cur.execute("INSERT OR REPLACE INTO kanbans(username,board_json) VALUES (?,?)", ("user", json.dumps(sample_board)))
        conn.commit()
    conn.close()
    return db_path


def get_kanban(username: str):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT board_json FROM kanbans WHERE username=?", (username,))
    row = cur.fetchone()
    conn.close()
    if row and row[0]:
        try:
            return json.loads(row[0])
        except Exception:
            return {}
    # default board shape matching frontend expectations (columns with cardIds and cards map)
    return {
        "columns": [
            {"id": "col-backlog", "title": "Backlog", "cardIds": []},
            {"id": "col-discovery", "title": "Discovery", "cardIds": []},
            {"id": "col-progress", "title": "In Progress", "cardIds": []},
            {"id": "col-review", "title": "Review", "cardIds": []},
            {"id": "col-done", "title": "Done", "cardIds": []},
        ],
        "cards": {}
    }


def save_kanban(username: str, board: dict):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO kanbans(username,board_json) VALUES (?,?)", (username, json.dumps(board)))
    conn.commit()
    conn.close()
