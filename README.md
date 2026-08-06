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

## GitHub Actions CI/CD
This repository includes a multi-stage pipeline in `.github/workflows/ci.yml`.

### Pipeline stages
- ✅ CI (Lint + Tests)
- ✅ Python Build
- ✅ Docker Build
- 🔐 Gitleaks
- 🔐 SonarQube (SAST)
- 🔐 Trivy (SCA)
- 📦 SBOM (Syft)
- 🛡️ Trivy Image Scan
- 📤 Docker Hub Push
- 🌐 OWASP ZAP (DAST)
- Deploy promotion stages: `dev`, `test`, `stage`, `prod`

### Environments
The workflow is designed to support multiple deployment environments with staged promotions:
- `dev`
- `test`
- `stage`
- `prod`

### Required GitHub Secrets
- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`
- `SONAR_ORGANIZATION`
- `SONAR_TOKEN`
- `SONAR_HOST_URL`

### Run locally with GitHub Actions
Use the GitHub UI or CLI to trigger the workflow manually via `workflow_dispatch`.
