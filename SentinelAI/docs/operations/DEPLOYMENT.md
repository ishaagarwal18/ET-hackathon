# SentinelAI Docker Deployment Guide

This guide describes the production-oriented Docker deployment for SentinelAI.

## Architecture

The Docker stack runs the platform as isolated services on a private bridge network:

- `nginx` is the public entry point and reverse proxies frontend, API, admin, schema, Swagger, static, and media routes.
- `frontend` builds the React/Vite application and serves the static bundle with Nginx.
- `backend` runs Django REST Framework through Gunicorn.
- `celery_worker` runs asynchronous background jobs with the same backend image.
- `mongodb` stores SentinelAI operational, security, model, report, and threat intelligence collections.
- `redis` is the Celery broker/result backend and can be reused for cache-oriented workloads later.

## Files

- `docker-compose.yml`: complete local/production Compose topology.
- `.env.example`: root environment template consumed by Compose.
- `backend/Dockerfile`: Django/Gunicorn runtime image.
- `frontend/Dockerfile`: Vite build plus static Nginx runtime image.
- `infrastructure/nginx/nginx.conf`: public reverse proxy configuration.
- `backend/gunicorn.conf.py`: production Gunicorn process settings.
- `backend/.env.docker.example`: backend-only environment reference.
- `frontend/.env.docker.example`: frontend build-time environment reference.

## Prerequisites

- Docker Engine 24 or newer.
- Docker Compose v2.
- At least 8 GB RAM available for local builds because AI dependencies such as FAISS, Transformers, and Sentence Transformers are heavy.
- A production host with firewall rules allowing only required ingress ports.

## Configure Environment

Copy the root template and update secrets before booting the stack:

```bash
cp .env.example .env
```

Required production changes:

- Replace `DJANGO_SECRET_KEY` with a long random value.
- Replace `MONGO_INITDB_ROOT_PASSWORD`.
- Set `DJANGO_ALLOWED_HOSTS` to real DNS names.
- Set `CORS_ALLOWED_ORIGINS` and `CSRF_TRUSTED_ORIGINS` to real frontend origins.
- Enable HTTPS settings when TLS is terminated at Nginx or an upstream load balancer:
  - `DJANGO_SECURE_SSL_REDIRECT=True`
  - `DJANGO_SESSION_COOKIE_SECURE=True`
  - `DJANGO_CSRF_COOKIE_SECURE=True`
  - `DJANGO_SECURE_HSTS_SECONDS=31536000`

The default Compose template disables Django HTTPS redirects so local health checks work over HTTP. Production deployments should enable TLS and secure cookies.

## Build And Start

From the `SentinelAI` directory:

```bash
docker compose --env-file .env build
docker compose --env-file .env up -d
```

Check service health:

```bash
docker compose ps
docker compose logs -f backend
docker compose logs -f celery_worker
```

Public endpoints:

- Frontend: `http://localhost/`
- Backend health: `http://localhost/api/v1/health/`
- Swagger: `http://localhost/api/docs/`
- API schema: `http://localhost/api/schema/`

## Database And Admin Operations

Run Django migrations for relational auth/admin tables:

```bash
docker compose exec backend python manage.py migrate
```

Create an admin user:

```bash
docker compose exec backend python manage.py createsuperuser
```

MongoDB is initialized with the database name from `MONGODB_NAME`. Application-level MongoDB indexes and collection validation should be applied by the existing model/index initialization commands or startup routines for each module.

## Health Checks

Compose includes health checks for every runtime dependency:

- MongoDB uses `db.adminCommand('ping')`.
- Redis uses `redis-cli ping`.
- Backend calls `/api/v1/health/`.
- Frontend calls `/healthz`.
- Nginx calls `/healthz`.
- Celery uses `celery inspect ping`.

Nginx waits for healthy backend and frontend services before becoming healthy.

## Production TLS

The provided Nginx configuration is HTTP-only so it can run locally without certificate material. For production, terminate TLS either:

- in front of this stack with a cloud load balancer, or
- inside `nginx` by mounting certificates and adding a `server` block on port `443`.

When TLS is active, set Django secure cookie and redirect flags in `.env`.

## Scaling

Scale stateless services horizontally:

```bash
docker compose up -d --scale backend=2 --scale celery_worker=2
```

If scaling backend containers behind the included Nginx service, remove fixed `container_name` values first because Docker Compose cannot scale services with static container names.

## Backups

MongoDB backup:

```bash
docker compose exec mongodb mongodump --archive=/tmp/sentinelai.archive --gzip --authenticationDatabase admin -u "$MONGO_INITDB_ROOT_USERNAME" -p "$MONGO_INITDB_ROOT_PASSWORD"
docker compose cp mongodb:/tmp/sentinelai.archive ./backups/sentinelai.archive
```

Persisted Docker volumes:

- `mongodb_data`
- `mongodb_config`
- `redis_data`
- `backend_media`
- `backend_reports`
- `backend_logs`
- `nginx_logs`

Include these volumes in the infrastructure backup policy.

## Updates

Deploy an update with:

```bash
docker compose pull
docker compose build --no-cache backend frontend celery_worker
docker compose up -d
docker compose exec backend python manage.py migrate
docker compose ps
```

Review `backend`, `celery_worker`, and `nginx` logs after each rollout.

## Security Checklist

- Do not commit `.env`.
- Use strong MongoDB credentials.
- Restrict direct access to MongoDB and Redis ports in production.
- Enable TLS and secure cookie settings.
- Rotate `DJANGO_SECRET_KEY` only with an explicit session/token invalidation plan.
- Ship logs to a centralized SIEM or log pipeline.
- Run container image vulnerability scanning before promotion.
- Use least-privilege host firewall and cloud security group rules.
