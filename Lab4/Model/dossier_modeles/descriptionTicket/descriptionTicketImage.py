from .descriptionTicket import DescriptionTicket

class DescriptionTicketImage(DescriptionTicket):
    _titre : str
    _filepath : str

    def __init__(self, id : int ,titre : str, filepath : str):
        super().__init__(id)
        self._titre = titre
        self._filepath = filepath

    def get_titre(self) -> str:
        return self._titre
    
    def get_description(self) -> str:
        return self._filepath

