FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
COPY main.py .

RUN pip install --no-cache-dir -r requirements.txt

RUN useradd -m appuser
USER appuser

CMD ["python", "main.py"]