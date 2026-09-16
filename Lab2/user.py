from ticket import Ticket

class User:
    _user_id : int
    _name : str
    _email : str
    _role : str
    _asign_tickets : list[Ticket]
    _created_tickets : list[Ticket]

    @property
    def user_id(self):
        return self._user_id

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
        self._user_id = user_id
        self._name = name
        self._email = email
        self._role = role
        self._asign_tickets = list[Ticket]()
        self._created_tickets = list[Ticket]()

    def create_ticket (self, ticket : Ticket):
        self._created_tickets.append(ticket)
    
    def view_ticket (self, ticket : Ticket):
        if not self._asign_tickets.__contains__(ticket):
            return

        print('---- Ticket ' + ticket.ticket_id + '----')
        print('Titre : ' + ticket.ticket_id)
        print('Description :' + ticket.description)
        print('Status :' + ticket.status)
        print('Priorité :' + ticket.priority)
        print('Date de création :' + ticket.creation_date.strftime("YYYY-MM-DD HH:mm:ss"))
        print('Date de modification :' + ticket.update_date.strftime("YYYY-MM-DD HH:mm:ss"))
    
    def update_ticket(self, ticket : Ticket):
        if not self._asign_tickets.__contains__(ticket):
            return

        if ticket.status == "ASSIGNÉ":
            ticket.update_status("VALIDATION")

        if ticket.status == "VALIDATION":
            ticket.update_status("TERMINÉ")