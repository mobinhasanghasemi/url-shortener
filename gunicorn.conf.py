import multiprocessing
import os

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
threads = 2
worker_class = "sync"
max_requests = 1000
max_requests_jitter = 50
timeout = 30
keepalive = 5
preload_app = True
graceful_timeout = 30

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shortUrl.settings')