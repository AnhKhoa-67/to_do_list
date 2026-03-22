from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional
from sqlmodel import Session
from app.schemas.todo import TodoRead, TodoCreate, TodoUpdate, TodoListResponse
from app.services.todo import todo_service
from app.core.db import get_session

router = APIRouter()

@router.get("/", response_model=TodoListResponse)
async def get_todos(
    *,
    session: Session = Depends(get_session),
    is_done: Optional[bool] = Query(None),
    q: Optional[str] = Query(None),
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0)
):
    items = todo_service.get_all(session, is_done=is_done, q=q, limit=limit, offset=offset)
    total = todo_service.get_total(session, is_done=is_done, q=q)
    return {"items": items, "total": total, "limit": limit, "offset": offset}

@router.post("/", response_model=TodoRead)
async def create_todo(*, session: Session = Depends(get_session), todo_in: TodoCreate):
    return todo_service.create(session, todo_in)

@router.get("/{id}", response_model=TodoRead)
async def get_todo(*, session: Session = Depends(get_session), id: int):
    todo = todo_service.get_by_id(session, id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.patch("/{id}", response_model=TodoRead)
async def update_todo(*, session: Session = Depends(get_session), id: int, todo_in: TodoUpdate):
    todo = todo_service.update(session, id, todo_in)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.delete("/{id}")
async def delete_todo(*, session: Session = Depends(get_session), id: int):
    if not todo_service.delete(session, id):
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted"}
