from pydantic import BaseModel

class UserSchemaIn(BaseModel):
    name: str
    address: str