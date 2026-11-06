from .descriptionTicket import DescriptionTicket

class DescriptionTicketTexte(DescriptionTicket):
    _titre : str
    _description : str
    
    def __init__(self, id : int | None, titre : str, description : str):
        super().__init__(id)
        self._titre = titre
        self._description = description

    def get_titre(self) -> str:
            return self._titre
    
    def get_description(self) -> str:
        return self._description


