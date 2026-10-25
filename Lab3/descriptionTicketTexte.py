from descriptionTicket import DescriptionTicket

class DescriptionTicketTexte(DescriptionTicket):
    _titre : str
    _description : str
    
    def __init__(self, titre : str, description : str):
        self._titre = titre
        self._description = description

    def get_titre(self):
            return self._titre
    
    def get_description(self):
        return self._description

