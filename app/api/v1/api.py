from fastapi import APIRouter

from app.api.v1.routers.predict import router as predict_router

router = APIRouter()


router.include_router(predict_router, prefix="/search", tags=["search"])
