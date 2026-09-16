from ticket import Ticket

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
    