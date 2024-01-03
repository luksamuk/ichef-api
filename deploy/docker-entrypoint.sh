#!/bin/sh
alembic upgrade head
exec uvicorn main:app --host 0.0.0.0 --port $API_PORT

