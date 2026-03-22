from typing import List, Optional
from sqlmodel import Session, select, func, col
from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate
from datetime import datetime

class TodoService:
    @staticmethod
    def get_all(session: Session, owner_id: int, is_done: Optional[bool] = None, 
                q: Optional[str] = None, limit: int = 10, offset: int = 0) -> List[Todo]:
        statement = select(Todo).where(Todo.owner_id == owner_id)
        if is_done is not None:
            statement = statement.where(Todo.is_done == is_done)
        if q:
            statement = statement.where(col(Todo.title).ilike(f"%{q}%"))
        
        statement = statement.offset(offset).limit(limit)
        results = session.exec(statement)
        return results.all()

    @staticmethod
    def get_total(session: Session, owner_id: int, is_done: Optional[bool] = None, 
                  q: Optional[str] = None) -> int:
        statement = select(func.count()).select_from(Todo).where(Todo.owner_id == owner_id)
        if is_done is not None:
            statement = statement.where(Todo.is_done == is_done)
        if q:
            statement = statement.where(col(Todo.title).ilike(f"%{q}%"))
        
        return session.exec(statement).one()

    @staticmethod
    def get_by_id(session: Session, todo_id: int) -> Optional[Todo]:
        return session.get(Todo, todo_id)

    @staticmethod
    def create(session: Session, todo_in: TodoCreate, owner_id: int) -> Todo:
        db_todo = Todo.model_validate(todo_in, update={"owner_id": owner_id})
        session.add(db_todo)
        session.commit()
        session.refresh(db_todo)
        return db_todo

    @staticmethod
    def update(session: Session, todo_id: int, todo_in: TodoUpdate) -> Optional[Todo]:
        db_todo = session.get(Todo, todo_id)
        if not db_todo:
            return None
        
        todo_data = todo_in.model_dump(exclude_unset=True)
        for key, value in todo_data.items():
            setattr(db_todo, key, value)
        
        db_todo.updated_at = datetime.utcnow()
        session.add(db_todo)
        session.commit()
        session.refresh(db_todo)
        return db_todo

    @staticmethod
    def delete(session: Session, todo_id: int) -> bool:
        db_todo = session.get(Todo, todo_id)
        if not db_todo:
            return False
        session.delete(db_todo)
        session.commit()
        return True

todo_service = TodoService()
