from sqlmodel import create_engine, Session
import os

DB_URL = os.getenv("DB_URL", "sqlite:///app/db/queries.db")

engine = create_engine(
    DB_URL,
    echo=True,
    connect_args={"check_same_thread": False}
)

def get_session():
    with Session(engine) as session:
        yield session
