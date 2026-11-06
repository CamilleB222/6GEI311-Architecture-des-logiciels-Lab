from pathlib import Path

from dossier_modeles import Ticket
from dossier_modeles import DescriptionTicketTexte
from dossier_modeles import DescriptionTicketImage
from dossier_modeles import User
from dossier_modeles import Admin

from schemas.ticketSchema import TicketResponseSchema
from schemas.descriptionSchema import DescriptionTexteSchema, DescriptionImageSchema
from schemas.userSchema import UserResponseSchema, AdminResponseSchema


def get_file_bytes(filepath: str | Path) -> bytes:
    path = Path(filepath)
    return path.read_bytes()

def map_description_to_schema(desc):
    if isinstance(desc, DescriptionTicketTexte):
        return DescriptionTexteSchema(id=desc.id,titre=desc.get_titre(), description=desc.get_description())
    elif isinstance(desc, DescriptionTicketImage):
        return DescriptionImageSchema(id=desc.id, titre=desc.get_titre(), filepath=desc.get_description(), binary_content=get_file_bytes(desc.get_description()))

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
    if isinstance(user, Admin):
        return AdminResponseSchema(
            id=user.id,
            name=user.name,
            email=user.email,
            role=user.role,
        )
    
    return UserResponseSchema(
        id=user.id,
        name=user.name,
        email=user.email,
        role=user.role,
    )