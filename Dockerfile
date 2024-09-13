FROM python:3.8-slim

WORKDIR /app
COPY requirements.txt /app/
RUN apt-get update \
    && apt-get install -y \
        build-essential \
        libpq-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . /app/
EXPOSE 5000
CMD flask db upgrade && gunicorn --bind 0.0.0.0:5000 app:app

