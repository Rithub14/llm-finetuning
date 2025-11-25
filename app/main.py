from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.streamlit_runner import start_streamlit
from app.db.init_db import init_db
from app.api.generate import router as generate_router
from app.api.health import router as health_router
import asyncio

from fastapi.responses import HTMLResponse
from fastapi import Request
import httpx

def create_app() -> FastAPI:
    app = FastAPI(
        title="Customer Support LLM API",
        version="0.1.10",
        description="FastAPI backend serving the finetuned Gemma2B LoRA model"
    )

    # --- CORS (Streamlit will call FastAPI internally) ---
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Init DB
    init_db()

    # Register routers
    app.include_router(health_router, prefix="/healthz", tags=["health"])
    app.include_router(generate_router, prefix="/generate", tags=["inference"])

    return app

app = create_app()

@app.get("/", response_class=HTMLResponse)
async def proxy_streamlit_root():
    """
    Redirects the root URL to Streamlit's frontend.
    """
    async with httpx.AsyncClient() as client:
        resp = await client.get("http://127.0.0.1:8001")
        return HTMLResponse(content=resp.text, status_code=resp.status_code)


@app.on_event("startup")
async def startup_event():
    """
    Runs once when FastAPI starts.
    This launches Streamlit in the background on port 8001.
    """
    asyncio.create_task(run_streamlit_background())


async def run_streamlit_background():
    """
    Wrapper because FastAPI does not allow direct sync calls inside startup.
    """
    await asyncio.sleep(1)  # wait 1 second so FastAPI fully boots
    start_streamlit()


@app.get("/{full_path:path}", response_class=HTMLResponse)
async def proxy_streamlit(full_path: str, request: Request):
    # Don’t proxy API routes
    if full_path.startswith("generate") or full_path.startswith("healthz"):
        return {"detail": "Not Found"}

    streamlit_url = f"http://127.0.0.1:8001/{full_path}"

    async with httpx.AsyncClient() as client:
        resp = await client.get(streamlit_url)
        return HTMLResponse(content=resp.text, status_code=resp.status_code)
