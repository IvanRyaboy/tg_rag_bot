# tg-rag-bot/Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# (опционально) системные зависимости для psycopg/cryptography
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# зависимости
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# код
COPY app ./app

# (без root)
RUN useradd -m app && chown -R app:app /app
USER app

EXPOSE 8080

# Запускаем через uvicorn (ваш main уже совместим)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
