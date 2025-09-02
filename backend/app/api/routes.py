from fastapi import APIRouter
from app.api.endpoints import datasets, analysis, cleaning, jobs

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(datasets.router, prefix="/datasets", tags=["datasets"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
api_router.include_router(cleaning.router, prefix="/cleaning", tags=["cleaning"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
