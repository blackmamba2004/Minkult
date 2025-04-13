#!/bin/bash
set -e

# Run migrations
source "$VENV_PATH/bin/activate" && python3.12 app/manage.py migrate

# Parse json
source "$VENV_PATH/bin/activate" && python3.12 app/manage.py parser data.json

# Start django
source "$VENV_PATH/bin/activate" && python3.12 app/manage.py runserver 0.0.0.0:8000
