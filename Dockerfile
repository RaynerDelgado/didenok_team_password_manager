FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev \ 
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./src ./src
COPY alembic.ini .
COPY alembic ./alembic

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]