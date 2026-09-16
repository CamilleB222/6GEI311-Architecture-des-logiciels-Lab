from ticket import Ticket
from user import User

class Admin:
    _admin_id : int
    _name : str
    _email : str
    _list_tickets : list[Ticket]


    def __init__(self, admin_id : int, name : str, email : str, list_tickets : list[Ticket]):
        self._admin_id = admin_id
        self._name = name
        self._email = email
        self._list_tickets = list_tickets


    @property
    def admin_id(self):
        return self._admin_id

    @property
    def name(self):
        return self._name

    @property
    def email(self):
        return self._email

    def assign_ticket(self, ticket : Ticket, user : User):
        ticket.assign_to(user)

    def close_ticket(self, ticket : Ticket):
        ticket.update_status("FERMER")

    def view_all_tickets(self) -> list[Ticket]:
        return self._list_tickets
    