from multiprocessing import cpu_count

# Socket Path
bind = 'unix:/hansung-grade-backend/gunicorn.sock'

# Worker Options
workers = cpu_count() * 2 + 1
worker_class = 'uvicorn.workers.UvicornWorker'

# Logging Options
loglevel = 'info'
accesslog = '/hansung-grade-backend/logs/access_log'
errorlog =  '/hansung-grade-backend/logs/error_log'