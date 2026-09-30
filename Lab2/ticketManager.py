from ticket import Ticket
from user import User
from admin import Admin

class TicketManager:
    _list_ticket : list[Ticket]
    _list_user_assignable : list[User]

    def __init__ (self):
        self._list_ticket = list[Ticket]()
        self._list_user_assignable = list[User]()

    @property
    def list_user_assignable(self):
        return self._list_user_assignable

    def view_all_ticket(self):
        return self._list_ticket

    def creat_ticket(self, user : User, ticket : Ticket):
        user.create_ticket(ticket)
        self._list_ticket.append(ticket)

    def view_ticket(self, user : User, ticket:Ticket) -> str:
        return user.view_ticket(ticket)

    def update_ticket(self, user : User, ticket:Ticket):
        user.update_ticket(ticket)

    def assign_Ticket(self, admin : Admin, user : User, ticket : Ticket):
        admin.assign_ticket(ticket, user)

    def close_ticket(self, admin : Admin, ticket : Ticket):
        admin.close_ticket(ticket)