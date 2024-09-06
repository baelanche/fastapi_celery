from celery import Celery
from celery.result import  AsyncResult
from app.databases.redis_client import RedisClient

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

Redis = RedisClient(host=REDIS_HOST, port=REDIS_PORT, db=DB_BACKEND)

def get_task_status(task_id: str, key: str = None):
    task_result = AsyncResult(task_id, app=celery_app)

    if task_result.state == 'PENDING':
        status = "Task is still processing"
        result = None
    elif task_result.state == 'FAILURE':
        status = "Task failed"
        result = None
    elif task_result.state == 'SUCCESS':
        status = "Task completed"
        result = task_result.result
        if key:
            Redis.setex(key, TASK_EXPIRATION_TIME, task_id)
    else:
        status = task_result.state
        result = None

    return {
        'task_id': task_id,
        'status': status,
        'result': result
    }