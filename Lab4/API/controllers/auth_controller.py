from fastapi import APIRouter, HTTPException, status
import secrets

from schemas.authSchema import ConnectRequestSchema, ConnectResponseSchema, DisconnectRequestSchema
from services.mappers import map_user_to_schema
from dossier_modeles import User
from program_list import dict_user_connect

from program_list import list_user, list_admin

router = APIRouter(tags=["Authentication"])

@router.post("/connect", response_model=ConnectResponseSchema)
def login(payload: ConnectRequestSchema):
    role = ""
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

    token = secrets.token_urlsafe(16)
    dict_user_connect[token] = user_entity
    
    return ConnectResponseSchema(
        role=role,
        token=token,
        user=map_user_to_schema(user_entity)
    )

@router.post("/disconnect")
def logout(payload: DisconnectRequestSchema):

    if dict_user_connect.pop(payload.token, None) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non connecter"
        )