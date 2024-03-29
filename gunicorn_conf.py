from multiprocessing import cpu_count

# Socket Path
bind = 'unix:/tmp/hansung_grade_backend.sock'

# Worker Options
workers = cpu_count() * 2 + 1
worker_class = 'uvicorn.workers.UvicornWorker'

# Logging Options
loglevel = 'info'
accesslog = '/app/logs/access.log'
errorlog =  '/app/logs/error.log'