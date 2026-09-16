from datetime import datetime

class Ticket:
    _ticket_id : int
    _title : str
    _description : str
    _status : str
    _priority : str
    _creation_date : datetime
    _update_date : datetime
    _list_commentaires : list[str]

    def __init__(self, ticket_id : int, title : str, description : str, priority : str, creation_date : datetime, update_date : datetime):
       self._ticket_id = ticket_id
       self._title = title
       self._description = description
       self._status = "OUVERT"
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

    def update_status(self, status : str):
        if self.status == "FERMER" or status == "FERMER":
            self._status = status

        if self.status == "OUVERT" and status == "ASSIGNÉ":
            self._status = status

        if self.status == "ASSIGNÉ" and status == "VALIDATION":
            self._status = status

        if self.status == "VALIDATION" and status == "TERMINÉ":
            self._status = status