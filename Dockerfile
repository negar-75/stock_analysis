FROM python:3.11-slim AS base

WORKDIR /app

RUN apt-get update && apt-get install -y gcc netcat-openbsd

#security reason
RUN pip install --no-cache-dir --upgrade pip setuptools wheel


COPY pyproject.toml .
COPY requirements.txt .
COPY alembic.ini .
COPY migrations/ migrations/

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/


RUN pip install -e .

# ---- test stage ----
FROM base AS test
COPY tests/ tests/
CMD ["pytest"]

# ---- prod stage ----
FROM base AS prod
EXPOSE 8000
CMD ["bash", "-c", "until nc -z $POSTGRES_HOST 5432; do sleep 1; done; alembic upgrade head && gunicorn -k uvicorn.workers.UvicornWorker stock_analysis.main:app --workers 4 --bind 0.0.0.0:8000"]