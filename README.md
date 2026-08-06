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

### Pipeline flow
```text
ci
  ├─> python_build
  ├─> sonarcloud
  └─> trivy_sca

python_build + sonarcloud + trivy_sca
  └─> docker_build

docker_build
  ├─> syft_sbom
  └─> trivy_image

trivy_image
  └─> docker_push

docker_push
  └─> run_container
         └─> owasp_zap

upload_reports
  depends on: sonarcloud, trivy_sca, syft_sbom, trivy_image, owasp_zap

deploy_dev
  └─> deploy_test
         └─> deploy_stage
                └─> deploy_prod
```

### Included scans and checks
- **CI**: Python linting with `ruff` and unit tests with `pytest`
- **Python Build**: packages the project with `python -m build --wheel`
- **SonarQube (SAST)**: static application security testing of source code
- **Trivy SCA**: file-system dependency vulnerability scan of the repository
- **Syft SBOM**: software bill of materials generation
- **Trivy Image Scan**: container image vulnerability scan
- **Docker Build**: builds the application container image
- **Docker Push**: pushes the built image to Docker Hub when credentials are configured
- **Run Docker Container**: starts the built image locally in the workflow for runtime checks
- **OWASP ZAP (DAST)**: baseline dynamic scan against the running application

### Current status
- `gitleaks` is currently disabled/commented out in the workflow for now.
- SonarQube is skipped automatically if `SONAR_HOST_URL` or `SONAR_TOKEN` are not provided.

### Required GitHub Secrets
- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`
- `SONAR_TOKEN` (optional)
- `SONAR_HOST_URL` (optional)

### Run locally with GitHub Actions
Use the GitHub UI or CLI to trigger the workflow manually via `workflow_dispatch`.
