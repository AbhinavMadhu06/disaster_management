#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Building Backend for Render Free Tier..."

# 1. Install Backend Dependencies
pip install -r requirements.txt

# 2. Collect Static Files
python manage.py collectstatic --no-input

# 3. Run Database Migrations (PostgreSQL)
python manage.py migrate

echo "Build Completed successfully."
