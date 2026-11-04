from fastapi import APIRouter, HTTPException, status
from schemas.ticketSchema import TicketAssignSchema, TicketCreateSchema, TicketResponseSchema, TicketUpdateSchema
from schemas.descriptionSchema import DescriptionCreateSchema, DescriptionImageSchema, DescriptionTexteSchema, DescriptionUnion
from services.mappers import map_user_to_schema
from dossier_modeles import Ticket

from program_list import ticket_manager

router = APIRouter(tags=["tickets"])

@router.post("/tickets", response_model=TicketResponseSchema)
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