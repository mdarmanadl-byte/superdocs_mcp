# SuperDocs Backend

FastAPI backend for the SuperDocs agentic document-analysis system.

## Tech Stack
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- pgvector
- LangGraph
- MCP
- AsyncPG
- LLM API

## Responsibilities
- Pile creation
- Document upload and ingestion
- Document parsing and chunking
- Vector storage and retrieval
- MCP document search
- Agent orchestration
- Answer generation
- Finding / contradiction detection
- Human-in-the-loop review
- Run state and checkpoint persistence
- Timing and LLM usage tracking

## Project Structure

```text
backend/
├── app/
│   ├── agents/
│   ├── api/
│   ├── models/
│   ├── services/
│   └── ...
├── test/
├── requirements.txt
└── README.md
```

## Setup

```bash
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file with the required database and LLM configuration.

## Run

```bash
uvicorn app.main:app --reload
```

API:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## Testing

```bash
pytest -q
```

The tests cover agent behavior, finding validation, concurrency isolation, and security-related behavior.

## Agent Workflow

```text
MCP Search
    ↓
Analyze
    ↓
Generate
    ↓
Finding
    ↓
Human Review
    ↓
Completed
```

LangGraph manages the stateful workflow and PostgreSQL provides persistent application state and checkpoints.
