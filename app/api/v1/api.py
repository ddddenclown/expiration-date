from fastapi import FastAPI
import uvicorn

from app.api.v1.routers.predict import router as predict_router

app = FastAPI(title="Product Shelf Life API", version="1.0.0")


app.include_router(predict_router, prefix="/search", tags=["search"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8007)
