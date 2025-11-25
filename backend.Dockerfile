# ---- Base image ----
    FROM python:3.12-slim

    # System dependencies for torch & transformers
    RUN apt-get update && apt-get install -y \
        git \
        build-essential \
        && rm -rf /var/lib/apt/lists/*
    
    # Set workdir
    WORKDIR /app
    
    # Copy project files
    COPY pyproject.toml .
    COPY app ./app
    COPY model ./model
    
    # Install uv
    RUN pip install uv
    
    # Install dependencies
    RUN uv pip install --system .
    
    # Expose backend API port
    EXPOSE 8000
    
    # Start FastAPI server
    CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
    