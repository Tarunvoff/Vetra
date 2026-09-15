FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./
COPY kvguard/ ./kvguard/

RUN pip install --upgrade pip && \
    pip install -e ".[simulation]"

EXPOSE 8080

CMD ["python", "-m", "kvguard.cli.main", "start", "--host", "0.0.0.0", "--port", "8080"]
