from descriptionTicket import DescriptionTicket

class DescriptionTicketTexte(DescriptionTicket):
    _description : str
    
    def __init__(self, description : str):
        self._description = description

    def get_description(self):
        return self._description

