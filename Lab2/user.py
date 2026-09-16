from ticket import Ticket

class User:
    _user_id : int
    _name : str
    _email : str
    _role : str
    _asign_tickets : list[Ticket]

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

    def create_ticket (ticket : Ticket):
        pass
    
    def view_ticket (ticket : Ticket):
        pass
    
    def update_ticket(ticket : Ticket):
        pass
