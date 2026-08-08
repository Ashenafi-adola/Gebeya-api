FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 1. Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# 2. Install Python dependencies (cached unless requirements.txt changes)
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# 3. Copy application code
COPY . .

# 4. Collect static files AFTER copying application code
RUN python manage.py collectstatic --no-input

# 5. Default port fallback (Render injects PORT dynamically)
ENV PORT=8000
EXPOSE $PORT

# 6. Execute via shell form to expand $PORT dynamically
CMD ["sh", "-c", "gunicorn config.wsgi:application --bind 0.0.0.0:${PORT}"]