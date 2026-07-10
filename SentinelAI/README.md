# SentinelAI

SentinelAI is an AI-powered Cyber Resilience Platform for SOC teams, security administrators, government officers, and auditors. It combines log collection, behavioral anomaly detection, threat intelligence retrieval, attack prediction, autonomous response simulation, incident reporting, and an executive SOC dashboard into one modular demonstration platform.

The project is built for a professional hackathon demo: it runs locally with Docker, exposes documented APIs, includes automated tests and coverage, and ships with fallback frontend data so the UI remains presentable even when live backend authentication is not configured.

## What It Demonstrates

- Secure JWT authentication with role-based access control.
- MongoDB-backed security collections, validation, indexes, and operational schemas.
- Log Collector Agent for Windows, Linux, firewall, JSON, CSV, and syslog data.
- Behavioral Anomaly Detection Engine using Scikit-learn Isolation Forest.
- Threat Intelligence Agent using LangChain-oriented retrieval, Sentence Transformers, and FAISS-ready vector store abstractions.
- AI Attack Prediction Agent with a rule engine, knowledge graph, scoring, and attack-chain visualization payloads.
- Autonomous Incident Response simulation with approvals and execution logs.
- Incident report generation with PDF, CSV, and JSON exports.
- React SOC dashboard with live API wiring, dark theme, charts, timeline, heat map, digital twin, and AI chat surfaces.
- Dockerized production-style deployment with Nginx, Django/Gunicorn, Celery, Redis, MongoDB, and frontend static serving.
- CI/CD workflow for backend tests, frontend tests, coverage artifacts, Docker Compose validation, and image builds.

## Architecture

```text
SentinelAI/
├── backend/                  Django, DRF, agents, AI engines, MongoDB access
├── frontend/                 React, Vite, TailwindCSS SOC interface
├── infrastructure/           Nginx, MongoDB, Redis, monitoring, IaC placeholders
├── docs/                     Architecture, operations, compliance, security docs
├── tests/                    Backend, API, AI, integration, security test suites
├── docker-compose.yml        Local production-like stack
├── pytest.ini                Backend test and coverage configuration
└── .github/workflows/        CI/CD pipeline
```

### Backend

The backend uses Django REST Framework as the API layer, MongoDB for flexible security documents, Redis/Celery for asynchronous execution, and modular agent packages for domain intelligence.

Key modules:

- `apps.authentication`: register, login, refresh, password reset, current user.
- `apps.logs`: log upload, listing, and detail APIs.
- `apps.behavior`: anomaly analysis API.
- `apps.threat_intelligence`: RAG-style threat chat APIs.
- `apps.attack_prediction`: next-attack prediction API.
- `apps.incidents`: simulated autonomous response APIs.
- `apps.reports`: incident report generation and downloads.
- `apps.dashboard`: aggregation APIs for SOC cards, charts, logs, timeline, and threat map.
- `agents/*`: clean agent services for logs, threat intelligence, response, SOC assistant, and prediction.
- `ai_engines/*`: model-specific AI logic.
- `database/mongodb`: collection schemas, validation, and indexes.

### Frontend

The frontend is a React/Vite SOC console with reusable layout, card, table, chart, notification, risk, attack timeline, threat graph, and digital twin components.

Important routes:

- `/dashboard`
- `/alerts`
- `/incidents`
- `/threat-intelligence`
- `/soc-assistant`
- `/assets`
- `/digital-twin`
- `/reports`
- `/settings`

### Infrastructure

Docker Compose starts:

- `nginx`
- `frontend`
- `backend`
- `celery_worker`
- `mongodb`
- `redis`

Nginx routes `/` to the React app and `/api/` to Django.

## Quick Start

From the `SentinelAI` directory:

```powershell
copy .env.example .env
docker compose --env-file .env up -d --build
```

Open:

- Frontend: `http://localhost/`
- Backend health: `http://localhost/api/v1/health/`
- Swagger UI: `http://localhost/api/docs/`
- OpenAPI schema: `http://localhost/api/schema/`

Check containers:

```powershell
docker compose --env-file .env ps
```

## Running Tests

Backend:

```bash
pip install -r backend/requirements-dev.txt
pytest
```

Frontend:

```bash
cd frontend
npm ci
npm run lint
npm run test:coverage
npm run build
```

Coverage outputs:

- `coverage/backend-coverage.xml`
- `coverage/backend-html/`
- `coverage/frontend/`

## CI/CD

GitHub Actions workflow:

```text
.github/workflows/ci-cd.yml
```

Pipeline stages:

- Backend unit, API, AI, and integration tests.
- Frontend lint, unit tests, coverage, and production build.
- Docker Compose config validation.
- Backend/frontend/Celery image build.
- Production deployment gate placeholder for future registry and infrastructure targets.

## Security Posture

Implemented controls:

- JWT authentication with role claims.
- Role-based API permissions for SOC Analyst, Security Admin, Government Officer, and Read Only Auditor.
- Standardized API success/error envelope.
- Request ID propagation through `X-Request-ID`.
- API request security logging with status and response time.
- Django production security settings for HSTS, secure cookies, proxy SSL header, content sniffing, and frame denial.
- Non-root backend and Celery containers.
- Environment-driven secrets and deployment settings.
- Simulated response actions only, with no real infrastructure mutation.

Demo warning:

The generated `.env` is suitable for local demonstration only. Replace `DJANGO_SECRET_KEY`, MongoDB credentials, allowed hosts, CORS origins, and TLS settings before real deployment.

## Documentation

- Deployment guide: `docs/operations/DEPLOYMENT.md`
- Production review: `docs/architecture/PRODUCTION_REVIEW.md`
- MongoDB schemas: `backend/database/mongodb/schemas.py`
- Sample API payloads: `backend/samples/`
- Test mock data: `tests/mock_data/`

## Known Demo Constraints

- Threat intelligence uses local/sample knowledge sources unless real feeds are connected.
- Autonomous response is intentionally simulated.
- Some frontend panels use fallback data when authenticated backend calls are unavailable.
- The default Docker image includes heavy AI dependencies; first builds can take several minutes.
- Production deployment still needs registry publishing, TLS certificate management, centralized logging, and real secrets management.

## Recommended Demo Flow

1. Start Docker Compose.
2. Open `http://localhost/` and show the SOC dashboard.
3. Open Swagger at `http://localhost/api/docs/`.
4. Demonstrate `/api/v1/health/`.
5. Register/login through auth APIs.
6. Upload a sample log from `backend/samples/logs/`.
7. Run behavioral anomaly analysis using `backend/samples/behavior_anomaly_request.json`.
8. Run attack prediction using `backend/samples/attack_prediction/predict_request.json`.
9. Generate an incident report using `backend/samples/reports/incident_report_request.json`.

## License

Hackathon demonstration project. Add a formal license before external distribution.
