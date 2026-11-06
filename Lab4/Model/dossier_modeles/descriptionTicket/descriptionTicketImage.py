from .descriptionTicket import DescriptionTicket

class DescriptionTicketImage(DescriptionTicket):
    _titre : str
    _filepath : str
    _binary_content : str

    def __init__(self, id : int ,titre : str, filepath : str, binary_content : str):
        super().__init__(id)
        self._titre = titre
        self._filepath = filepath
        self._binary_content = binary_content

    def get_titre(self) -> str:
        return self._titre
    
    def get_description(self) -> str:
        return self._filepath

    def get_binary_content(self) -> str:
        return self._binary_content

