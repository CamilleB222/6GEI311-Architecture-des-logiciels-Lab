# API/schemas/ticket_schema.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from dossier_modeles import StatutTicket
from .descriptionSchema import DescriptionUnion, DescriptionCreateSchema

# --- SCHÉMA DE RÉPONSE (GET) ---
class TicketResponseSchema(BaseModel):
    ticket_id: int
    title: str
    description_ini: str
    list_description: list[DescriptionUnion] = []
    status: StatutTicket
    priority: str
    creation_date: datetime
    update_date: datetime
    user_assign: str

    model_config = ConfigDict(from_attributes=True)


# --- SCHÉMA DE CRÉATION (POST /tickets) ---
class TicketCreateSchema(BaseModel):
    title: str
    description_initiale: str
    priority: str


# --- SCHÉMA DE MISE À JOUR (PUT/ticket/{id}) ---
class TicketUpdateSchema(BaseModel):
    title: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[StatutTicket] = None
    user_assign: Optional[str] = None


# --- SCHÉMA POUR ASSIGNER UN UTILISATEUR ---
class TicketAssignSchema(BaseModel):
    user_id: int