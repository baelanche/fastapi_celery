from fastapi import APIRouter
from celery.result import AsyncResult
from app.configs.celery_config import celery_app, Redis, get_task_status
from app.databases.redis_client import RedisClient
from app.models.sample_model import Sample

router = APIRouter(
    prefix="/celery",
)

@router.post('/delay')
async def create_delay_task():
    task = celery_app.send_task('delay_task')

    return {
        'task_id': task.id,
        'status': 'PENDING'
    }

@router.get('/delay')
async def get_delay_task_result(task_id: str):
    return get_task_status(task_id)

@router.post('/delay/cache')
async def create_delay_with_cache_task(sample: Sample):
    def handle_exists(cached_task_id: str):
        task_result = AsyncResult(cached_task_id, app=celery_app)
        if task_result.state == 'SUCCESS':
            return {
                'task_id': cached_task_id,
                'status': task_result.state,
                'result': task_result.result
            }
        else:
            Redis.delete(sample.id)
            handle_not_exists()

    def handle_not_exists():
        task = celery_app.send_task('delay_task_with_cache')
        return {
            'task_id': task.id,
            'status': 'PENDING'
        }
    
    return Redis.cache_exists_or_not(sample.id, handle_exists, handle_not_exists)
        
@router.get('/delay/cache')
async def get_delay_task_with_cache_result(id: str, task_id: str):
    return get_task_status(task_id, id)
