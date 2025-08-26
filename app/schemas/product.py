from pydantic import BaseModel
from typing import Optional


class ProductQuery(BaseModel):
    ItemName: str
    Description: Optional[str] = ""

class ProductResponse(BaseModel):
    LifeTime: int

class ErrorResponse(BaseModel):
    error: str
    detail: str
    