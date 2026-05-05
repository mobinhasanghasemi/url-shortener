#!/usr/bin/env python
import os
import sys
import multiprocessing
import subprocess
import time
import signal

def run_gunicorn():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shortUrl.settings')
    
    cpu_count = multiprocessing.cpu_count()
    worker_count = cpu_count * 2 + 1
    
    cmd = [
        sys.executable, '-m', 'gunicorn',
        '--bind', '0.0.0.0:8000',
        '--workers', str(worker_count),
        '--threads', '2',
        '--timeout', '30',
        '--max-requests', '1000',
        '--max-requests-jitter', '50',
        '--preload',
        'shortUrl.wsgi:application'
    ]
    
    process = subprocess.Popen(cmd)
    return process

def run_uvicorn():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shortUrl.settings')
    
    cpu_count = multiprocessing.cpu_count()
    worker_count = cpu_count * 2
    
    cmd = [
        sys.executable, '-m', 'uvicorn',
        '--host', '0.0.0.0',
        '--port', '8000',
        '--workers', str(worker_count),
        '--loop', 'uvloop',
        '--http', 'httptools',
        'shortUrl.asgi:application'
    ]
    
    process = subprocess.Popen(cmd)
    return process

if __name__ == '__main__':
    print(f"Starting with {multiprocessing.cpu_count() * 2 + 1} workers...")
    
    try:
        process = run_gunicorn()
        signal.signal(signal.SIGINT, lambda s, f: process.terminate())
        signal.signal(signal.SIGTERM, lambda s, f: process.terminate())
        process.wait()
    except KeyboardInterrupt:
        print("\nShutting down workers...")
        process.terminate()
        process.wait()