#!/bin/sh
poetry install
alembic upgrade head
exec python main.py