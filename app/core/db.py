from sqlmodel import create_engine, Session, SQLModel
from app.core.config import settings

sqlite_file_name = "db.sqlite3"
sqlite_url = f"sqlite:///./{sqlite_file_name}"

engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    SQLModel.metadata.create_all(engine)
