from sqlmodel import SQLModel
from app.db.session import engine

def init_db() -> None:
    """
    Creates all database tables defined using SQLModel.
    Called once on FastAPI startup.
    """
    SQLModel.metadata.create_all(engine)
