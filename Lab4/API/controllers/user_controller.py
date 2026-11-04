from fastapi import APIRouter, HTTPException, status, Depends
from schemas.userSchema import UserResponseSchema
from schemas.ticketSchema import TicketResponseSchema

from services.mappers import map_user_to_schema
from dependencies import verify_custom_token

from program_list import list_user

from dossier_modeles import User

router = APIRouter(tags=["Users"], dependencies=[Depends(verify_custom_token)])

@router.get("/users", response_model=list[UserResponseSchema])
def get_users():
    list_user_schema = list[UserResponseSchema]()

    for user in list_user:
        list_user_schema.append(map_user_to_schema(user))

    return  list_user_schema

@router.get("/user/{user_id}", response_model=UserResponseSchema, status_code=status.HTTP_200_OK)
def get_user(user_id: int):
    user_return : User | None
    
    for user in list_user:
        if user.id == user_id:
            user_return = user

    if not user_return:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    
    return map_user_to_schema(user)

@router.get("/user/{user_id}/tickets", response_model=list[TicketResponseSchema])
def get_user_tickets(user_id : int):
    user_return : User | None

    for user in list_user:
            if user.id == user_id:
                user_return = user

    if not user_return:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    list_ticket_user = user.asign_tickets
    list_ticket_response = list[TicketResponseSchema]()

    for ticket in list_ticket_user:
        list_ticket_response.append()

    pass