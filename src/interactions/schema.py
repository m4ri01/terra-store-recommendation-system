from pydantic import BaseModel
from uuid import UUID

class InteractionsSchemaIn(BaseModel):
    user_id: UUID
    time_spent: int
    page_views: int
