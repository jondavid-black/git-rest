# syntax=docker/dockerfile:1
FROM python:3.12-slim

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy project files
COPY . /app

# Install uv and project dependencies
RUN pip install uv && uv pip install -e .[dev]

# Expose port for Gunicorn
EXPOSE 8000

# Environment variables (override in production)
ENV GIT_REST_SECRET_KEY=changeme-super-secret-key
ENV GIT_REST_WORKDIR=/data/repos

# Entrypoint: Gunicorn with Flask app
CMD ["uv", "run", "gunicorn", "-b", "0.0.0.0:8000", "src.git_rest.main:app"]
