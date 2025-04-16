#!/bin/bash
set -e
exec uvicorn bday_service.app:app --host 0.0.0.0 --port 8000
