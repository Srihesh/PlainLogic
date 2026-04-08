FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml /app/pyproject.toml
COPY uv.lock /app/uv.lock
COPY inference.py /app/inference.py
COPY src /app/src
COPY server /app/server

RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -e .

CMD ["sh", "-c", "uvicorn resilienceos.server:app --host 0.0.0.0 --port ${PORT:-7860}"]
