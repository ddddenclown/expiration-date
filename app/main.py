from fastapi import FastAPI
import uvicorn

from app.api.v1 import router


app = FastAPI(title="Product LifeTime API", version="1.0.0")

app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8007)
