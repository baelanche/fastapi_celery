from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from app.routers import home_router
from app.routers.api import celery_router

app = FastAPI(
    default_response_class=ORJSONResponse,
)

origins = [
	"*"
]

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
    allow_credentials=True,
	allow_methods=['*'],
	allow_headers=['*'],
)

app.include_router(home_router.router, prefix='')
app.include_router(celery_router.router, prefix='/api')