from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime
from pathlib import Path


from schemas.ticketSchema import TicketAssignSchema, TicketCreateSchema, TicketResponseSchema, TicketUpdateSchema, TicketCreateResponseSchema
from schemas.descriptionSchema import DescriptionCreateSchema, DescriptionImageSchema, DescriptionTexteSchema, DescriptionUnion, DescriptionUpdateSchema


from dossier_modeles import Ticket, StatutTicket, Admin, User, DescriptionTicketTexte, DescriptionTicketImage, DescriptionTicket
from dependencies import verify_custom_token, verify_custom_token_admin
from program_list import ticket_manager, list_user, dict_user_connect, generer_nouvel_id
from services.mappers import map_ticket_to_schema, map_description_to_schema

def get_ticket_by_id(ticket_id : int):
    # Trouver le ticket
    ticket_trouver : Ticket | None = None
    for ticket in ticket_manager.view_all_ticket():
            if ticket.ticket_id == ticket_id:
                ticket_trouver = ticket
                break
    
    if ticket_trouver is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket introuvable"
        )

    return ticket_trouver

def get_description_by_id(list_description : list[DescriptionTicket],description_id : DescriptionTicket):
    # Trouver la description
    description_trouver : DescriptionTicket | None = None
    for description in list_description:
            if description.id == description_id:
                description_trouver = description
    
    if description_trouver is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Description introuvable"
        )

    return description_trouver

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
    ticket_response : TicketResponseSchema = map_ticket_to_schema(get_ticket_by_id(ticket_id))

    return ticket_response

@router.put("/ticket/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_ticket(ticket_id : int, payload : TicketUpdateSchema, token = Depends(verify_custom_token)):
    user = dict_user_connect[token]
    old_ticket : Ticket = get_ticket_by_id(ticket_id)

    # Vérification du statut du ticket
    if old_ticket.status == StatutTicket.OUVERT and not payload.status == StatutTicket.OUVERT and not (isinstance(user, Admin) and payload.status == StatutTicket.FERMER) :
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
        ticket_manager.close_ticket(user,new_ticket)

@router.delete("/ticket/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket(ticket_id : int):
    ticket_trouver : Ticket = get_ticket_by_id(ticket_id)

    ticket_manager.view_all_ticket().remove(ticket_trouver)

@router.post("/ticket/{ticket_id}/assign", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(verify_custom_token_admin)])
def assign_ticket(ticket_id : int, payload : TicketAssignSchema,token = Depends(verify_custom_token)):
    admin = dict_user_connect[token]
    user_assign : User | None = None
    
    for user in list_user:
            if user.id == payload.user_id:
                user_assign = user

    if not user_assign:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    ticket_trouver = get_ticket_by_id(ticket_id)

    ticket_manager.assign_Ticket(admin, user_assign, ticket_trouver)

@router.get("/ticket/{ticket_id}/descriptions", response_model=list[DescriptionUnion])
def get_descriptions(ticket_id : int):
    ticket_trouver : Ticket = get_ticket_by_id(ticket_id)

    list_description_ticket_schema : list[DescriptionUnion] = list[DescriptionUnion]()

    for description in ticket_trouver.list_description:
         list_description_ticket_schema.append(map_description_to_schema(description))

    return list_description_ticket_schema

@router.post("/ticket/{ticket_id}/descriptions", status_code=status.HTTP_201_CREATED)
def create_descripsion(ticket_id : int, payload : DescriptionCreateSchema):
    ticket_trouver : Ticket = get_ticket_by_id(ticket_id)

    if payload.type_description == "texte":
        id = generer_nouvel_id()
        ticket_trouver.list_description.append(DescriptionTicketTexte(id ,payload.titre, payload.contenu))
    elif payload.type_description == "image":
        # Enregistrer l'image sur le disc
        if payload.binary_content is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Il faut un flux binaire pour ajouter une image"
            )
        
        BASE_DIR = Path(__file__).resolve().parent
        image_dir = BASE_DIR / "image"
        image_dir.mkdir(parents=True, exist_ok=True)

        nom_variable = payload.contenu
        extension = "png"

        output_path = image_dir / f"{nom_variable}.{extension}"

        with open(output_path, "wb") as file:
            file.write(payload.binary_content)

        id = generer_nouvel_id()

        ticket_trouver.list_description.append(DescriptionTicketImage(id ,payload.titre, output_path, payload.binary_content))
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="type de description non prise en charge"
        )

@router.get("/ticket/{ticket_id}/description/{description_id}", response_model=DescriptionUnion)
def get_description(ticket_id : int, description_id : int):
    ticket_trouver : Ticket = get_ticket_by_id(ticket_id)
    description_trouver :DescriptionTicket = get_description_by_id(ticket_trouver.list_description, description_id)
    

    return map_description_to_schema(description_trouver)

@router.put("/ticket/{ticket_id}/description/{description_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_description(ticket_id : int, description_id : int, payload : DescriptionUpdateSchema):
    ticket_trouver : Ticket = get_ticket_by_id(ticket_id)
    description_trouver : DescriptionTicket = get_description_by_id(ticket_trouver.list_description, description_id)

    if payload.type_description == "texte":
        ticket_trouver.list_description.remove(description_trouver)
        ticket_trouver.list_description.append(DescriptionTicketTexte(description_id ,payload.titre, payload.contenu))
    elif payload.type_description == "image":
        # Enregistrer l'image sur le disc
        if payload.binary_content is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Il faut un flux binaire pour ajouter une image"
            )
        
        BASE_DIR = Path(__file__).resolve().parent
        image_dir = BASE_DIR / "image"
        image_dir.mkdir(parents=True, exist_ok=True)

        nom_variable = payload.contenu
        extension = "png"

        output_path = image_dir / f"{nom_variable}.{extension}"

        with open(output_path, "wb") as file:
            file.write(payload.binary_content)

        ticket_trouver.list_description.remove(description_trouver)
        ticket_trouver.list_description.append(DescriptionTicketImage(description_id, payload.titre, output_path))
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="type de description non prise en charge"
        )

@router.delete("/ticket/{ticket_id}/description/{description_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_description(ticket_id : int, description_id : int):
    ticket_trouver : Ticket = get_ticket_by_id(ticket_id)
    description_trouver : DescriptionTicket = get_description_by_id(ticket_trouver.list_description, description_id)

    ticket_trouver.list_description.remove(description_trouver)
