from datetime import datetime

class Ticket:
    _ticket_id : int
    _title : str
    _description : str
    _status : str
    _priority : str
    _creation_date : datetime
    _update_date : datetime

    def __init__(self, ticket_id : int, title : str, description : str, status : str, priority : str, creation_date : datetime, update_date : datetime):
       self._ticket_id = ticket_id
       self._title = title
       self._description = description
       self._status = status
       self._priority = priority
       self._creation_date = creation_date
       self._update_date = update_date

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