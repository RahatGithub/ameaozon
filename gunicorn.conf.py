import multiprocessing

# Bind to all interfaces — nginx container reverse-proxies to this
bind = "0.0.0.0:8000"

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
