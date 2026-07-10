FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential curl libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

RUN groupadd --system sentinelai \
    && useradd --system --gid sentinelai --home-dir /app --shell /usr/sbin/nologin sentinelai

COPY . .

RUN mkdir -p /app/staticfiles /app/media /app/logs /app/generated_reports \
    && chown -R sentinelai:sentinelai /app

USER sentinelai

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/v1/health/', timeout=4)"

CMD ["gunicorn", "config.wsgi:application", "-c", "gunicorn.conf.py"]
