import multiprocessing

# Bind to localhost — nginx will reverse-proxy to this
bind = "127.0.0.1:8000"

# CPX22: 4 vCPU — (2 * cores) + 1
workers = multiprocessing.cpu_count() * 2 + 1

# Restart workers after this many requests to prevent memory leaks
max_requests = 1000
max_requests_jitter = 50

# Kill worker if it hangs longer than 30s
timeout = 30

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
