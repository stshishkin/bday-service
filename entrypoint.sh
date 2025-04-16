#!/bin/bash
set -e
poetry run alembic upgrade head &&
    exec uvicorn bday_service.app:app --host 0.0.0.0 --port 8000
