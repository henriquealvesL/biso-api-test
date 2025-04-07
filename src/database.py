from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./movies.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

Base = declarative_base()

def get_session():
    with Session(engine) as session:
        yield session
