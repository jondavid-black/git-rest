#!/bin/bash
# Entrypoint script for git-rest Docker container
set -e

# Ensure required env vars are set
: "${GIT_REST_SECRET_KEY:?GIT_REST_SECRET_KEY not set}"
: "${GIT_REST_WORKDIR:?GIT_REST_WORKDIR not set}"

# Run migrations or setup here if needed

# Start Gunicorn with Flask app
exec uv run gunicorn -b 0.0.0.0:8000 src.git_rest.main:app
