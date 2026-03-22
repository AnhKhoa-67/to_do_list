from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.schemas.tag import TagRead

class TodoBase(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: Optional[str] = None
    is_done: Optional[bool] = False
    due_date: Optional[datetime] = None

class TodoCreate(TodoBase):
    tags: Optional[List[str]] = [] # List of tag names

class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = None
    is_done: Optional[bool] = None
    due_date: Optional[datetime] = None
    tags: Optional[List[str]] = None # List of tag names

class TodoRead(TodoBase):
    id: int
    created_at: datetime
    updated_at: datetime
    owner_id: int
    tags: List[TagRead] = []

    class Config:
        from_attributes = True

class TodoList(BaseModel):
    items: List[TodoRead]
    total: int
