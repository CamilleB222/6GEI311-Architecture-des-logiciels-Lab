from datetime import datetime
from descriptionTicket import DescriptionTicket
from descriptionTicketImage import DescriptionTicketImage
from descriptionTicketTexte import DescriptionTicketTexte
from statutTicket import StatutTicket

class Ticket:
    _ticket_id : int
    _title : str
    _list_description : list[DescriptionTicket]
    _status : StatutTicket
    _priority : str
    _creation_date : datetime
    _update_date : datetime
    _list_commentaires : list[str]

    def __init__(self, ticket_id : int, title : str, description_initiale : str, priority : str, creation_date : datetime, update_date : datetime):
        self._ticket_id = ticket_id
        self._title = title
        self._description = list[DescriptionTicket]()
        self._description.append(self.add_description(description_initiale))   
        self._status = StatutTicket.OUVERT
        self._priority = priority
        self._creation_date = creation_date
        self._update_date = update_date
        self._list_commentaires = list[str]()

    @property
    def ticket_id(self):
        return self._ticket_id

    @property
    def title(self):
        return self._title

    @property
    def description(self):
        return self._description

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

    def assign_to(self, user):
        user.asign_tickets.append(self)

    def update_status(self, status : StatutTicket):
        if self.status == StatutTicket.FERMER or status == StatutTicket.FERMER:
            self._status = status
            return

        if (self.status == status-1):# Si le Statut actuelle est avant le statut qu'on veut aller
            self.status = status

    def add_description(self, type_description : type, description : str):
        if (type_description == DescriptionTicketTexte):
            description_texte = DescriptionTicketTexte(description)
            self._list_description.append(description_texte)

        elif (type_description == DescriptionTicketImage):
            description_image = DescriptionTicketImage(description)
            self._list_description.append(description_image)