# API/services/mappers.py
from dossier_modeles import Ticket
from dossier_modeles import DescriptionTicketTexte
from dossier_modeles import DescriptionTicketImage
from dossier_modeles import User
from dossier_modeles import Admin

from schemas.ticketSchema import TicketResponseSchema
from schemas.descriptionSchema import DescriptionTexteSchema, DescriptionImageSchema
from schemas.userSchema import UserResponseSchema, AdminResponseSchema

def map_description_to_schema(desc):
    if isinstance(desc, DescriptionTicketTexte):
        return DescriptionTexteSchema(titre=desc.get_titre(), description=desc.get_description())
    elif isinstance(desc, DescriptionTicketImage):
        return DescriptionImageSchema(titre=desc.get_titre(), filepath=desc.get_description())

def map_ticket_to_schema(ticket: Ticket) -> TicketResponseSchema:
    return TicketResponseSchema(
        ticket_id=ticket.ticket_id,
        title=ticket.title,
        description_ini=ticket.description_ini,
        list_description=[map_description_to_schema(d) for d in ticket.list_description],
        status=ticket.status,
        priority=ticket.priority,
        creation_date=ticket.creation_date,
        update_date=ticket.update_date,
        user_assign=ticket.user_assign
    )

def map_user_to_schema(user: User | Admin):
    assigned_ids = [t.ticket_id for t in user.asign_tickets]
    if isinstance(user, Admin):
        return AdminResponseSchema(
            id=user.id,
            name=user.name,
            email=user.email,
            role=user.role,
            assigned_ticket_ids=assigned_ids
        )
    return UserResponseSchema(
        id=user.id,
        name=user.name,
        email=user.email,
        role=user.role,
        assigned_ticket_ids=assigned_ids
    )