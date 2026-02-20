FROM python:3.11-slim AS base

WORKDIR /app

RUN apt-get update && apt-get install -y gcc


COPY pyproject.toml .
COPY requirements.txt .

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
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "stock_analysis.main:app", "--workers", "4", "--bind", "0.0.0.0:8000"]