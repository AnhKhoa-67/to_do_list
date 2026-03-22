from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional, List
from sqlmodel import Session, select
from app.schemas.todo import TodoRead, TodoCreate, TodoUpdate, TodoListResponse
from app.models.todo import Todo
from app.models.user import User
from app.services.todo import todo_service
from app.core.db import get_session
from app.api.v1.deps import get_current_user

router = APIRouter()

@router.get("/", response_model=TodoListResponse)
async def get_todos(
    *,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    is_done: Optional[bool] = Query(None),
    q: Optional[str] = Query(None),
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0)
):
    # Let's just update the service logic in the next step to accept owner_id
    items = todo_service.get_all(session, owner_id=current_user.id, is_done=is_done, q=q, limit=limit, offset=offset)
    total = todo_service.get_total(session, owner_id=current_user.id, is_done=is_done, q=q)
    return {"items": items, "total": total, "limit": limit, "offset": offset}

@router.post("/", response_model=TodoRead)
async def create_todo(
    *, 
    session: Session = Depends(get_session), 
    current_user: User = Depends(get_current_user),
    todo_in: TodoCreate
):
    return todo_service.create(session, todo_in, owner_id=current_user.id)

@router.get("/{id}", response_model=TodoRead)
async def get_todo(
    *, 
    session: Session = Depends(get_session), 
    current_user: User = Depends(get_current_user),
    id: int
):
    todo = todo_service.get_by_id(session, id)
    if not todo or todo.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.patch("/{id}", response_model=TodoRead)
async def update_todo(
    *, 
    session: Session = Depends(get_session), 
    current_user: User = Depends(get_current_user),
    id: int, 
    todo_in: TodoUpdate
):
    todo = todo_service.get_by_id(session, id)
    if not todo or todo.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo_service.update(session, id, todo_in)

@router.delete("/{id}")
async def delete_todo(
    *, 
    session: Session = Depends(get_session), 
    current_user: User = Depends(get_current_user),
    id: int
):
    todo = todo_service.get_by_id(session, id)
    if not todo or todo.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo_service.delete(session, id)
    return {"message": "Todo deleted"}
