# DevSecOps Demo API

This project is a realistic FastAPI backend used for learning DevSecOps practices.

## Features
- FastAPI REST API with OpenAPI docs
- SQLite + SQLAlchemy models
- Alembic-ready structure
- CRUD for products and users
- JWT login endpoint
- pytest test suite

## Run locally
```bash
python -m pip install -r requirements-dev.txt
python -m uvicorn app.main:app --reload
```

## Run tests
```bash
python -m pytest -q
```

## Docker
```bash
docker compose up --build
```
