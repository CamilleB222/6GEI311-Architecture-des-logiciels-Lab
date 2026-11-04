from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime


from schemas.ticketSchema import TicketAssignSchema, TicketCreateSchema, TicketResponseSchema, TicketUpdateSchema, TicketCreateResponseSchema
from schemas.descriptionSchema import DescriptionCreateSchema, DescriptionImageSchema, DescriptionTexteSchema, DescriptionUnion
from services.mappers import map_user_to_schema
from dossier_modeles import Ticket, StatutTicket, Admin
from dependencies import verify_custom_token, verify_custom_token_admin
from program_list import dict_user_connect


from program_list import ticket_manager
from services.mappers import map_ticket_to_schema

router = APIRouter(tags=["tickets"], dependencies=[Depends(verify_custom_token)])


@router.get("/tickets", response_model=list[TicketResponseSchema], dependencies=[Depends(verify_custom_token_admin)])
def get_tickets():
    list_ticket_response_schema = list[TicketResponseSchema]()

    for ticket in ticket_manager.view_all_ticket():
        list_ticket_response_schema.append(map_ticket_to_schema(ticket))

    return list_ticket_response_schema


@router.post("/tickets", response_model=TicketCreateResponseSchema ,status_code=status.HTTP_201_CREATED, dependencies=[Depends(verify_custom_token_admin)])
def create_ticket(payload : TicketCreateSchema, token = Depends(verify_custom_token_admin)):
    if not len(ticket_manager.view_all_ticket()) == 0:
        ticket_id = max(ticket.ticket_id for ticket in ticket_manager.view_all_ticket()) + 1
    else:
        ticket_id = 1

    ticket = Ticket(ticket_id, payload.title, payload.description_initiale, payload.priority, datetime.now(), datetime.now())
    ticket_manager.creat_ticket(dict_user_connect[token],ticket)

    return TicketCreateResponseSchema(ticket_id=ticket_id)

@router.get("/ticket/{ticket_id}", response_model=TicketResponseSchema)
def get_ticket(ticket_id : int):
    ticket_response : TicketResponseSchema | None = None

    for ticket in ticket_manager.view_all_ticket():
        if ticket.ticket_id == ticket_id:
            ticket_response = map_ticket_to_schema(ticket)

    if ticket_response is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket introuvable"
        )

    return ticket_response

@router.put("/ticket/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_ticket(ticket_id : int, payload : TicketUpdateSchema, token = Depends(verify_custom_token_admin)):
    user = dict_user_connect[token]
    old_ticket : Ticket | None = None

    # Trouver l'ancien ticket
    for ticket in ticket_manager.view_all_ticket():
            if ticket.ticket_id == ticket_id:
                old_ticket = ticket
    
    if old_ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket introuvable"
        )

    # Vérification du statut du ticket
    if old_ticket.status == StatutTicket.OUVERT and not payload.status == StatutTicket.OUVERT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le statut du ticket est a ouvert donc il est imposible de modifier le statut avant de l'assigner"
        )
    elif old_ticket.status == StatutTicket.FERMER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Imposible de modifier un ticket fermer"
        )
    elif old_ticket.status > payload.status:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Imposible de retourner a un status précédent"
        )

    # Vérification de fermer ticket juste les admins
    if payload.status == StatutTicket.FERMER and not isinstance(user, Admin):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Il faut être admin pour fermer un ticket"
        )
    
    new_ticket = Ticket(ticket_id, payload.title, payload.description_ini, payload.priority, old_ticket.creation_date, datetime.now(), payload.status)
    ticket_manager.update_ticket_complet(user, old_ticket, new_ticket)

    if payload.status == StatutTicket.FERMER:
        ticket_manager.close_ticket(user,ticket)

@router.delete("/ticket/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket(ticket_id : int):
    ticket_trouver : Ticket | None = None
    # Trouver le ticket
    for ticket in ticket_manager.view_all_ticket():
            if ticket.ticket_id == ticket_id:
                ticket_trouver = ticket
    
    if ticket_trouver is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket introuvable"
        )
    
    ticket_manager.view_all_ticket().remove(ticket_trouver)