from dossier_modeles import Ticket, User, Admin

class TicketManager:
    _list_ticket : list[Ticket]
    _list_user_assignable : list[User]

    def __init__ (self, list_ticket : list[Ticket], list_user_assignable : list[User]):
        self._list_ticket = list_ticket
        self._list_user_assignable = list_user_assignable

    @property
    def list_user_assignable(self):
        return self._list_user_assignable

    def view_all_ticket(self):
        return self._list_ticketgit 

    def creat_ticket(self, user : User, ticket : Ticket):
        user.create_ticket(ticket)
        self._list_ticket.append(ticket)

    def update_ticket_complet(self, user : User, old_ticket : Ticket, new_ticket : Ticket):
        ticket_id = old_ticket.ticket_id
        
        for i, ticket in enumerate(self._list_ticket):
            if ticket.ticket_id == ticket_id:
                self._list_ticket[i] = new_ticket

        for utilisateur in self._list_user_assignable:
            for i, ticket in enumerate(utilisateur._asign_tickets):
                if ticket.ticket_id == ticket_id:
                    utilisateur._asign_tickets[i] = new_ticket

    def view_ticket(self, user : User, ticket:Ticket) -> str:
        return user.view_ticket(ticket)

    def update_ticket(self, user : User, ticket:Ticket):
        user.update_ticket(ticket)

    def register_user(self, user : User):
        if user not in self._list_user_assignable:
            self._list_user_assignable.append(user)

    def assign_Ticket(self, admin : Admin, user : User, ticket : Ticket):
        if not ticket.user_assign == "":
            for utilisateur in self._list_user_assignable:
                if utilisateur.name == ticket.user_assign:
                    utilisateur.remove_ticket(ticket.ticket_id)
        
        admin.assign_ticket(ticket, user)

    def close_ticket(self, admin : Admin, ticket : Ticket):
        admin.close_ticket(ticket, self._list_user_assignable)