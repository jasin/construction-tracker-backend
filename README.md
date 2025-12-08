# Construction Tracker - Python Backend

FastAPI backend for the Construction Tracker application with PostgreSQL (Supabase) and real-time WebSocket support.

## Quick Start

1. Create virtual environment: `python -m venv venv`
2. Activate: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and configure with your Supabase credentials
5. Run migrations: `alembic upgrade head`
6. Run server: `uvicorn app.main:app --reload`
7. Visit API docs: http://localhost:8000/docs

## Tech Stack

- **FastAPI** 0.115.5 - Modern Python web framework
- **SQLAlchemy** 2.0.36 - ORM for database operations
- **Alembic** 1.14.0 - Database migrations
- **PostgreSQL** (Supabase) - Database
- **WebSockets** 14.1 - Real-time updates
- **Pydantic** 2.10.3 - Data validation

## Project Structure

```
app/
├── models/         # SQLAlchemy ORM models
├── schemas/        # Pydantic schemas (validation)
├── repositories/   # Data access layer (CRUD)
├── routers/        # API endpoint handlers
├── services/       # Business logic
├── middleware/     # Custom middleware
├── utils/          # Utility functions
└── constants/      # Constants and enums

migrations/         # Alembic database migrations
tests/              # Unit and integration tests
scripts/            # Utility scripts
```

## Phase 1 Complete

- [x] Project structure created
- [x] Virtual environment set up
- [x] Dependencies installed
- [x] FastAPI application initialized  
- [x] Alembic migrations configured
- [x] Git repository initialized
- [x] Configuration files created

## Next Steps

**Phase 2**: Create database models (Task, Project, User, RFI, etc.)

See `PYTHON_BACKEND_MIGRATION.md` for complete migration documentation.

## Development

```bash
# Run server with auto-reload
uvicorn app.main:app --reload

# Generate migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Run tests
pytest

# Format code
black app/
```

## Documentation

- API Docs: http://localhost:8000/docs (Swagger UI)
- Alternative Docs: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health
