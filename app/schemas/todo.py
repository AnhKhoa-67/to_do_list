from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class TodoBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    is_done: bool = False

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = None
    is_done: Optional[bool] = None

class TodoRead(TodoBase):
    id: int
    created_at: datetime
    updated_at: datetime

class TodoListResponse(BaseModel):
    items: List[TodoRead]
    total: int
    limit: int
    offset: int
