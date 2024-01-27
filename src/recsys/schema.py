from pydantic import BaseModel
from uuid import UUID

class RecsysPredictIn(BaseModel):
    user_id: UUID