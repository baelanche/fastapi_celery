from celery import Celery

REDIS_HOST = 'redis'
REDIS_PORT = 6379
DB_BROKER = 0
DB_BACKEND = 1
TASK_EXPIRATION_TIME = 300

celery_app = Celery(
    'celery_template', 
    broker=f'redis://{REDIS_HOST}:{REDIS_PORT}/{DB_BROKER}', 
    backend=f'redis://{REDIS_HOST}:{REDIS_PORT}/{DB_BACKEND}',
    result_expires=TASK_EXPIRATION_TIME
)

from app.tasks import delay_task