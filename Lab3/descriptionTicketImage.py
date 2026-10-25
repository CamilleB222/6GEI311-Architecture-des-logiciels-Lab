from descriptionTicket import DescriptionTicket

class DescriptionTicketImage(DescriptionTicket):
    _titre : str
    _filepath : str

    def __init__(self, titre : str, filepath : str):
        self._titre = titre
        self._filepath = filepath

    def get_titre(self):
        return self._titre
    
    def get_description(self):
        return self._filepath

