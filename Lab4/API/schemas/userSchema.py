from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Literal

class UserResponseSchema(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str

    model_config = ConfigDict(from_attributes=True)

class AdminResponseSchema(UserResponseSchema):
    pass