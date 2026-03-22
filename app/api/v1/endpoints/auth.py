from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from app.core.db import get_session
from app.core.security import create_access_token
from app.schemas.user import UserRead, UserCreate, Token
from app.services.user import user_service

router = APIRouter()

@router.post("/register", response_model=UserRead)
def register(user_in: UserCreate, session: Session = Depends(get_session)):
    user = user_service.get_by_email(session, user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_service.create(session, user_in)

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = user_service.authenticate(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    return {"access_token": create_access_token(user.id), "token_type": "bearer"}
