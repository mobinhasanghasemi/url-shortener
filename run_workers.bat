@echo off
title URL Shortener - Multi Worker Server

set DJANGO_SETTINGS_MODULE=shortUrl.settings

echo ========================================
echo Starting URL Shortener with Multiple Workers
echo ========================================

set WORKERS=4
set THREADS=2
set PORT=8000

echo Workers: %WORKERS%
echo Threads per worker: %THREADS%
echo Port: %PORT%
echo.

python -m gunicorn --bind 0.0.0.0:%PORT% --workers %WORKERS% --threads %THREADS% --timeout 30 --max-requests 1000 --preload shortUrl.wsgi:application

pause