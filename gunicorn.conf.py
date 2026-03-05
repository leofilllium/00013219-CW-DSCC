"""Gunicorn configuration for MediTrack."""
import multiprocessing

# Bind to 0.0.0.0:8000
bind = "0.0.0.0:8000"

# Workers: 2 * CPU cores + 1
workers = multiprocessing.cpu_count() * 2 + 1

# Timeout (seconds)
timeout = 120

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
