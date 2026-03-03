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

# 4. Create Superuser automatically if credentials are provided in Render Env Vars
if [[ -n "${DJANGO_SUPERUSER_USERNAME}" && -n "${DJANGO_SUPERUSER_PASSWORD}" && -n "${DJANGO_SUPERUSER_EMAIL}" ]]; then
  echo "Creating superuser from Environment Variables..."
  python manage.py createsuperuser --noinput || echo "Superuser might already exist."
fi

echo "Build Completed successfully."
