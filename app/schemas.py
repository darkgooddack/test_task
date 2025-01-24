from pydantic import BaseModel

class ProductRequest(BaseModel):
    artikul: str

class ProductResponse(BaseModel):
    artikul: str
    name: str
    price: float
    rating: float
    stock_count: int

    class Config:
        from_attributes = True