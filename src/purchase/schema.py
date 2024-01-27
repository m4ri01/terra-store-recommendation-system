from pydantic import BaseModel
from uuid import UUID

class UserPurchaseSchemaIn(BaseModel):
    user_id: UUID
    product_id: UUID
    ratings: float