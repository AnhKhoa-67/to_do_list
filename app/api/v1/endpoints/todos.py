from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import Optional
from sqlmodel import Session, select
from app.schemas.todo import TodoRead, TodoCreate, TodoUpdate, TodoList
from app.models.todo import Todo
from app.models.user import User
from app.services.todo import todo_service
from app.core.db import get_session
from app.api.v1.deps import get_current_user

router = APIRouter()

@router.get("/", response_model=TodoList)
def get_todos(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    is_done: Optional[bool] = Query(None),
    q: Optional[str] = Query(None),
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0)
):
    items = todo_service.get_all(session, owner_id=current_user.id, is_done=is_done, q=q, limit=limit, offset=offset)
    total = todo_service.get_total(session, owner_id=current_user.id, is_done=is_done, q=q)
    return {"items": items, "total": total}

@router.get("/today", response_model=TodoList)
def get_today_todos(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0)
):
    items = todo_service.get_all(session, owner_id=current_user.id, limit=limit, offset=offset, filter_type="today")
    total = todo_service.get_total(session, owner_id=current_user.id, filter_type="today")
    return {"items": items, "total": total}

@router.get("/overdue", response_model=TodoList)
def get_overdue_todos(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0)
):
    items = todo_service.get_all(session, owner_id=current_user.id, limit=limit, offset=offset, filter_type="overdue")
    total = todo_service.get_total(session, owner_id=current_user.id, filter_type="overdue")
    return {"items": items, "total": total}

@router.post("/", response_model=TodoRead)
def create_todo(
    todo_in: TodoCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return todo_service.create(session, todo_in, owner_id=current_user.id)

@router.get("/{todo_id}", response_model=TodoRead)
def get_todo(
    todo_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    todo = todo_service.get_by_id(session, todo_id)
    if not todo or todo.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.patch("/{todo_id}", response_model=TodoRead)
def update_todo(
    todo_id: int,
    todo_in: TodoUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    todo = todo_service.get_by_id(session, todo_id)
    if not todo or todo.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo_service.update(session, todo_id, todo_in)

@router.delete("/{todo_id}")
def delete_todo(
    todo_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    todo = todo_service.get_by_id(session, todo_id)
    if not todo or todo.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo_service.delete(session, todo_id)
    return {"message": "Todo deleted"}
