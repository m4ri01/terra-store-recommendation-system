from pydantic import BaseModel

class ProductSchemaIn(BaseModel):
    product_name: str
    category: str
    price: int
    ratings: float