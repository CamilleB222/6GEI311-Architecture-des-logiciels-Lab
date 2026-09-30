from ticket import Ticket
from statutTicket import StatutTicket

class User:
    _id : int
    _name : str
    _email : str
    _role : str
    _asign_tickets : list[Ticket]
    _created_tickets : list[Ticket]

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def email(self):
        return self._email

    @property
    def role(self):
        return self._role

    @property
    def asign_tickets(self):
        return self._asign_tickets
        

    def __init__ (self, user_id : int, name : str, email : str, role : str):
        self._id = user_id
        self._name = name
        self._email = email
        self._role = role
        self._asign_tickets = list[Ticket]()
        self._created_tickets = list[Ticket]()

    def create_ticket (self, ticket : Ticket):
        self._created_tickets.append(ticket)
    
    def view_ticket (self, ticket : Ticket) -> str:
        if not self._asign_tickets.__contains__(ticket):
            return ""
        
        ticket_string : str = ""

        ticket_string += ('---- Ticket ' + str(ticket.ticket_id) + ' ----') + "\n"
        ticket_string +=('Titre : ' + ticket.title) + "\n"
        num_description : int = 1
        for description in ticket.list_description:
            
            ticket_string +=('Description ' + str(num_description) + ' : ' + description.get_description()) + "\n"
            num_description += 1

        ticket_string +=('Status : ' + ticket.status.name) + "\n"
        ticket_string +=('Priorité : ' + ticket.priority) + "\n"
        ticket_string +=('Date de création : ' + ticket.creation_date.strftime("%Y-%m-%d %H:%M:%S")) + "\n"
        ticket_string +=('Date de modification : ' + ticket.update_date.strftime("%Y-%m-%d %H:%M:%S")) + "\n"

        return ticket_string
    
    def update_ticket(self, ticket : Ticket):
        if not self._asign_tickets.__contains__(ticket):
            return

        if ticket.status == StatutTicket.ASSIGNÉ:
            ticket.update_status(StatutTicket.VALIDATION)

        elif ticket.status == StatutTicket.VALIDATION:
            ticket.update_status(StatutTicket.TERMINE)