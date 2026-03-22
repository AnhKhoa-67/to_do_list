from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True, min_length=3, max_length=100)
    description: Optional[str] = Field(default=None)
    is_done: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    owner_id: int = Field(foreign_key="user.id")
    owner: Optional["User"] = Relationship(back_populates="todos")
