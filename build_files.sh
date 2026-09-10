#!/bin/bash
set -e
echo "Installing Node dependencies..."
npm install
echo "Building Tailwind CSS..."
npx tailwindcss -i ./static/src/input.css -o ./static/dist/output.css --minify
echo "Installing Python dependencies..."
pip install -r requirements.txt
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear