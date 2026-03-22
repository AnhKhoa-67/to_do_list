from typing import List, Optional
from sqlmodel import Session, select, func, col
from app.models.todo import Todo
from app.models.tag import Tag, TodoTagLink
from app.schemas.todo import TodoCreate, TodoUpdate
from datetime import datetime, date, time

class TodoService:
    @staticmethod
    def _get_or_create_tags(session: Session, tag_names: List[str]) -> List[Tag]:
        tags = []
        for name in tag_names:
            statement = select(Tag).where(Tag.name == name)
            tag = session.exec(statement).first()
            if not tag:
                tag = Tag(name=name)
                session.add(tag)
                session.flush()
            tags.append(tag)
        return tags

    @staticmethod
    def get_all(session: Session, owner_id: int, is_done: Optional[bool] = None, 
                q: Optional[str] = None, limit: int = 10, offset: int = 0,
                filter_type: Optional[str] = None) -> List[Todo]:
        statement = select(Todo).where(Todo.owner_id == owner_id)
        
        if is_done is not None:
            statement = statement.where(Todo.is_done == is_done)
        if q:
            statement = statement.where(col(Todo.title).ilike(f"%{q}%"))
        
        now = datetime.utcnow()
        today_start = datetime.combine(date.today(), time.min)
        today_end = datetime.combine(date.today(), time.max)

        if filter_type == "overdue":
            statement = statement.where(Todo.due_date < now).where(Todo.is_done == False)
        elif filter_type == "today":
            statement = statement.where(Todo.due_date >= today_start).where(Todo.due_date <= today_end)

        statement = statement.offset(offset).limit(limit)
        results = session.exec(statement)
        return results.all()

    @staticmethod
    def get_total(session: Session, owner_id: int, is_done: Optional[bool] = None, 
                  q: Optional[str] = None, filter_type: Optional[str] = None) -> int:
        statement = select(func.count()).select_from(Todo).where(Todo.owner_id == owner_id)
        if is_done is not None:
            statement = statement.where(Todo.is_done == is_done)
        if q:
            statement = statement.where(col(Todo.title).ilike(f"%{q}%"))
        
        now = datetime.utcnow()
        today_start = datetime.combine(date.today(), time.min)
        today_end = datetime.combine(date.today(), time.max)

        if filter_type == "overdue":
            statement = statement.where(Todo.due_date < now).where(Todo.is_done == False)
        elif filter_type == "today":
            statement = statement.where(Todo.due_date >= today_start).where(Todo.due_date <= today_end)
        
        return session.exec(statement).one()

    @staticmethod
    def get_by_id(session: Session, todo_id: int) -> Optional[Todo]:
        return session.get(Todo, todo_id)

    @staticmethod
    def create(session: Session, todo_in: TodoCreate, owner_id: int) -> Todo:
        todo_data = todo_in.model_dump(exclude={"tags"})
        db_todo = Todo(**todo_data, owner_id=owner_id)
        
        if todo_in.tags:
            db_todo.tags = TodoService._get_or_create_tags(session, todo_in.tags)
            
        session.add(db_todo)
        session.commit()
        session.refresh(db_todo)
        return db_todo

    @staticmethod
    def update(session: Session, todo_id: int, todo_in: TodoUpdate) -> Optional[Todo]:
        db_todo = session.get(Todo, todo_id)
        if not db_todo:
            return None
        
        todo_data = todo_in.model_dump(exclude_unset=True, exclude={"tags"})
        for key, value in todo_data.items():
            setattr(db_todo, key, value)
        
        if todo_in.tags is not None:
            db_todo.tags = TodoService._get_or_create_tags(session, todo_in.tags)
        
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
