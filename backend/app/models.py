from pydantic import BaseModel
from typing import List, Dict, Any


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    token: str


class Card(BaseModel):
    id: str
    title: str
    details: str = ""


class Column(BaseModel):
    id: str
    title: str
    cardIds: List[str] = []


class KanbanBoard(BaseModel):
    columns: List[Column]
    cards: Dict[str, Card]
