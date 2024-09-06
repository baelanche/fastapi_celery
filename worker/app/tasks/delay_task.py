from app.main import celery_app
import time

@celery_app.task(name='delay_task')
def delay():
    time.sleep(10)
    return 'delay_task completed'

@celery_app.task(name='delay_task_with_cache')
def delay_with_cache():
    time.sleep(10)
    return 'delay_task_with_cache completed'