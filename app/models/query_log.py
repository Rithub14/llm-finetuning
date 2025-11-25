from sqlmodel import SQLModel, Field, Column, JSON
from datetime import datetime
from typing import Optional, Dict


class QueryLog(SQLModel, table=True):
    """
    Stores every user query and the generated LLM response.
    Useful for analytics, debugging, retraining data, monitoring.
    """

    id: Optional[int] = Field(default=None, primary_key=True)

    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="UTC time the query was processed"
    )

    query_text: str = Field(nullable=False)
    response_text: str = Field(nullable=False)

    latency_ms: float = Field(
        default=0.0,
        description="Inference time in milliseconds"
    )

    model_version: str = Field(
        default="checkpoint-939",
        description="Which model / LoRA version produced the result"
    )
