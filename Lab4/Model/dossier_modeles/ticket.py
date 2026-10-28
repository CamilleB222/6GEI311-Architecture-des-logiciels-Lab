from datetime import datetime
from pydantic import BaseModel
from .descriptionTicket import DescriptionTicket
from .descriptionTicketImage import DescriptionTicketImage
from .descriptionTicketTexte import DescriptionTicketTexte
from .statutTicket import StatutTicket

class Ticket(BaseModel):
    _ticket_id : int
    _title : str
    _description_ini : str
    _list_description : list[DescriptionTicket]
    _status : StatutTicket
    _priority : str
    _creation_date : datetime
    _update_date : datetime
    _list_commentaires : list[str]
    _user_assign : str

    def __init__(self, ticket_id : int, title : str, description_initiale : str, priority : str, creation_date : datetime, update_date : datetime, status:StatutTicket = StatutTicket.OUVERT):
        self._ticket_id = ticket_id
        self._title = title
        self._description_ini = description_initiale   
        self._list_description = list[DescriptionTicket]()
        self._status = status
        self._priority = priority
        self._creation_date = creation_date
        self._update_date = update_date
        self._list_commentaires = list[str]()
        self._user_assign = ""

    @property
    def ticket_id(self):
        return self._ticket_id

    @property
    def title(self):
        return self._title

    @property
    def description_ini(self):
        return self._description_ini

    @property
    def list_description(self):
        return self._list_description

    @property
    def status(self):
        return self._status

    @property
    def priority(self):
        return self._priority

    @property
    def creation_date(self):
        return self._creation_date

    @property
    def update_date(self):
        return self._update_date

    @property
    def user_assign(self):
        return self._user_assign

    def assign_to(self, user):
        user.asign_tickets.append(self)
        self._user_assign = user.name

    def update_status(self, status : StatutTicket):
        if self.status == StatutTicket.FERMER or status == StatutTicket.FERMER:
            self._status = status
            return

        if (self.status == status-1):# Si le Statut actuelle est avant le statut qu'on veut aller
            self._status = status

    def add_description(self, type_description : type, titre : str, description : str):
        if (type_description == DescriptionTicketTexte):
            description_texte = DescriptionTicketTexte(titre, description)
            self._list_description.append(description_texte)

        elif (type_description == DescriptionTicketImage):
            description_image = DescriptionTicketImage(titre, description)
            self._list_description.append(description_image)