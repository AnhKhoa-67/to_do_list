from typing import Optional
from sqlmodel import Session, select
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password

class UserService:
    @staticmethod
    def get_by_email(session: Session, email: str) -> Optional[User]:
        return session.exec(select(User).where(User.email == email)).first()

    @staticmethod
    def create(session: Session, user_in: UserCreate) -> User:
        db_user = User(
            email=user_in.email,
            hashed_password=get_password_hash(user_in.password),
        )
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user

    @staticmethod
    def authenticate(session: Session, email: str, password: str) -> Optional[User]:
        user = UserService.get_by_email(session, email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

user_service = UserService()
