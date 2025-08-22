import multiprocessing

# Gunicorn configuration
workers = 1
worker_class = "sync"
worker_connections = 1000
timeout = 120  # 2 minutes timeout
keepalive = 5