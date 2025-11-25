FROM python:3.12-slim

WORKDIR /frontend

# Install streamlit + requests
RUN pip install streamlit requests

# Copy frontend files
COPY frontend ./frontend

EXPOSE 8501

CMD ["streamlit", "run", "frontend/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
