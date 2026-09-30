from ticket import Ticket

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
        ticket_string +=('Description : ' + ticket.description) + "\n"
        ticket_string +=('Status : ' + ticket.status) + "\n"
        ticket_string +=('Priorité : ' + ticket.priority) + "\n"
        ticket_string +=('Date de création : ' + ticket.creation_date.strftime("%Y-%m-%d %H:%M:%S")) + "\n"
        ticket_string +=('Date de modification : ' + ticket.update_date.strftime("%Y-%m-%d %H:%M:%S")) + "\n"

        return ticket_string
    
    def update_ticket(self, ticket : Ticket):
        if not self._asign_tickets.__contains__(ticket):
            return

        if ticket.status == "ASSIGNÉ":
            ticket.update_status("VALIDATION")

        elif ticket.status == "VALIDATION":
            ticket.update_status("TERMINÉ")