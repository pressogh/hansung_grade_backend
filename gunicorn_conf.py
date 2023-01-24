from multiprocessing import cpu_count

# Socket Path
bind = 'unix:/hansung-grade-backend/gunicorn.sock'

# Worker Options
workers = cpu_count() * 2 + 1
worker_class = 'uvicorn.workers.UvicornWorker'

# Logging Options
loglevel = 'info'
accesslog = './logs/access_log'
errorlog =  './logs/error_log'