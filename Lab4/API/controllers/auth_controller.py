# API/controllers/auth_controller.py
from fastapi import APIRouter, HTTPException, status
from schemas.authSchema import ConnectRequestSchema, ConnectResponseSchema
from services.mappers import map_user_to_schema
from dossier_modeles import User

from program_list import list_user, list_admin

router = APIRouter(tags=["Authentication"])

@router.post("/connect", response_model=ConnectResponseSchema)
def login(payload: ConnectRequestSchema):
    user_entity = None
    for user in list_user:
        if user.name == payload.name and not payload.password == "":
            user_entity = user
            role = "user"
            break

    if not user_entity:
        for admin in list_admin:
            if admin.name == payload.name and not payload.password == "":
                user_entity = admin
                role = "admin"
                break
    
    if not user_entity:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants invalides"
        )
    
    return ConnectResponseSchema(
        role=role,
        user=map_user_to_schema(user_entity)
    )