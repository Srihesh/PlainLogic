FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml /app/pyproject.toml
COPY src /app/src
COPY scripts /app/scripts

RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -e .

CMD ["python", "scripts/baseline_inference.py", "--seed", "7", "--output", "outputs/baseline_report.json"]
