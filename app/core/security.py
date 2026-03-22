import hashlib
import os
from datetime import datetime, timedelta
from typing import Optional, Union, Any
from jose import jwt
from app.core.config import settings

ALGORITHM = "HS256"
SECRET_KEY = "your-secret-key"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(subject: Union[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_password_hash(password: str) -> str:
    # Simple SHA256 hashing for compatibility
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return get_password_hash(plain_password) == hashed_password
