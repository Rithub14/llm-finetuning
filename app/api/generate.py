from fastapi import APIRouter, Depends, BackgroundTasks
from pydantic import BaseModel
from sqlmodel import Session
from loguru import logger

from app.services.inference import generate_answer
from app.db.session import get_session
from app.models.query_log import QueryLog


router = APIRouter()


# ---------------------------
# Request & Response Schemas
# ---------------------------

class GenerateRequest(BaseModel):
    query: str


class GenerateResponse(BaseModel):
    response: str
    model_version: str = "checkpoint-939"


# ---------------------------
# Background Task: Log Query
# ---------------------------

def log_query_task(
    session: Session,
    query: str,
    response: str,
    latency_ms: float = 0.0,
):
    try:
        entry = QueryLog(
            query_text=query,
            response_text=response,
            latency_ms=latency_ms,
            model_version="checkpoint-939",
        )
        session.add(entry)
        session.commit()
        logger.info("Query logged successfully.")
    except Exception as e:
        logger.error(f"Failed to log query: {e}")


# ---------------------------
# Generate Endpoint
# ---------------------------

@router.post("/", response_model=GenerateResponse)
async def generate(
    payload: GenerateRequest,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
):
    logger.info(f"Received query: {payload.query}")

    # Run inference
    response_text = generate_answer(payload.query)

    # Background logging (non-blocking)
    background_tasks.add_task(
        log_query_task,
        session=session,
        query=payload.query,
        response=response_text,
        latency_ms=0.0,
    )

    return GenerateResponse(response=response_text)
