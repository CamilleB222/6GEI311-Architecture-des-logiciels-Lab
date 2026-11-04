# API/schemas/auth_schema.py
from pydantic import BaseModel
from .userSchema import UserResponseSchema

class ConnectRequestSchema(BaseModel):
    name : str
    password: str

class ConnectResponseSchema(BaseModel):
    role : str
    token : str
    user: UserResponseSchema

class DisconnectRequestSchema(BaseModel):
    token : str