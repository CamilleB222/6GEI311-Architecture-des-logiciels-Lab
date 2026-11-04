# API/controllers/auth_controller.py
from fastapi import APIRouter, HTTPException, status
from schemas.authSchema import ConnectRequestSchema, ConnectResponseSchema
from services.mappers import map_user_to_schema
from dossier_modeles import User

router = APIRouter(tags=["Authentication"])

@router.post("/connect", response_model=ConnectResponseSchema)
def login(payload: ConnectRequestSchema):
    # 1. Vérification de l'utilisateur (exemple avec ta logique métier)
    user_entity = User(1, "Xavier", "xavier400@outlook.fr","Utilisateur")
    
    if not user_entity:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants invalides"
        )
    
    # 2. Construction de la réponse avec l'objet User et son rôle
    return ConnectResponseSchema(
        role="user",
        user=map_user_to_schema(user_entity)
    )