#!/bin/sh
echo "Waiting for Kafka to be available... Sleep to 20 seconds"
sleep 20

echo "Installing dependencies with Poetry..."
poetry install || { echo "Poetry installation failed"; exit 1; }

echo "Running Alembic migrations..."
alembic upgrade head || { echo "Alembic migrations failed"; exit 1; }

echo "Starting FastAPI application..."
exec python main.py