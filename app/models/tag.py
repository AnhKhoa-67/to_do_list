from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class TodoTagLink(SQLModel, table=True):
    todo_id: Optional[int] = Field(default=None, foreign_key="todo.id", primary_key=True)
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id", primary_key=True)

class Tag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    
    todos: List["Todo"] = Relationship(back_populates="tags", link_model=TodoTagLink)
