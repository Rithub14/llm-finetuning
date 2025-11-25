📘 Customer Support LLM — Finetuned Gemma 2B (LoRA)

A lightweight, end-to-end AI assistant for customer support queries.
Built using FastAPI, Streamlit, LoRA-finetuned Gemma-2B, and SQLite logging.

🚀 Overview

This project fine-tunes Google Gemma-2B-IT using LoRA on a customer-support dataset (Bitext).
It exposes a clean backend API and a simple chat UI for interacting with the model.

Key Features

🧠 LoRA-finetuned Gemma-2B model for intent-based support responses

⚡ FastAPI backend with clean modular structure

💬 Streamlit chat interface (runs automatically when backend starts)

🗄 SQLite database logging of all user queries & model responses

🔧 Modular codebase: services, routers, models, utils

🧹 Production-style project structure + packaging

🏗 Architecture
+------------------+       +-----------------------------+
|   Streamlit UI   | <---> |        FastAPI API          |
+------------------+       +-------------+---------------+
                                      |
                                      v
                         +---------------------------+
                         |  LoRA-finetuned Gemma-2B  |
                         +---------------------------+
                                      |
                                      v
                             +----------------+
                             |   SQLite DB    |
                             +----------------+

📦 Project Structure
llm_finetuning/
├── app/
│   ├── api/            # FastAPI routes
│   ├── core/           # Streamlit launcher
│   ├── db/             # SQLite + session
│   ├── models/         # SQLModel ORM
│   ├── services/       # Inference logic
│   ├── utils/          # Prompt builder
│   └── main.py         # FastAPI entrypoint
│
├── frontend/
│   └── app.py          # Streamlit UI
│
├── model/
│   └── adapters/       # LoRA checkpoint
│
├── pyproject.toml
├── Makefile
├── README.md
└── .gitignore

⚙️ Installation
1️⃣ Create environment
uv venv
source .venv/bin/activate

2️⃣ Install dependencies
uv sync

3️⃣ Start backend + UI
uvicorn app.main:app --reload


Streamlit automatically runs in background on port 8001.

Open browser:

http://localhost:8000/

🧪 Example API Call
curl -X POST "http://localhost:8000/generate/" \
     -H "Content-Type: application/json" \
     -d '{"query": "How do I track my order?"}'


Response:

{
  "response": "You can track your order by visiting..."
}

🗄 Database Logging

Every query is stored in SQLite:

user query

model response

timestamp

latency

model version

View manually:

sqlite3 app/db/queries.db
SELECT * FROM querylog;

📚 Model Fine-Tuning

The LoRA training was performed using:

transformers

peft

SFTTrainer (from TRL)

Kaggle → Bitext Customer Support dataset

Output adapters are stored in:

model/adapters/checkpoint-939/

📄 License

MIT License (add LICENSE file if needed).