from ticket import Ticket
from user import User
from statutTicket import StatutTicket

class Admin(User):

    def __init__(self, admin_id : int, name : str, email : str):
        super().__init__(admin_id, name, email, "admin")


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
        ticket.update_status(StatutTicket.ASSIGNÉ)

    def close_ticket(self, ticket : Ticket):
        ticket.update_status(StatutTicket.FERMER)
    