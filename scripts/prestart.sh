#! /usr/bin/env bash

set -e
set -x

# Let the DB start
python "${PROJECT_NAME}/backend_pre_start.py"

# Run migrations
alembic upgrade head

# Create initial data in DB
python "${PROJECT_NAME}/initial_data.py"

