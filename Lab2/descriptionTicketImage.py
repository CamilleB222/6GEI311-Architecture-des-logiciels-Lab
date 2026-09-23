from descriptionTicket import DescriptionTicket

class DescriptionTicketImage(DescriptionTicket):
    _filepath : str

    def __init__(self, filepath : str):
        self._filepath = filepath

    def get_description(self):
        return self._filepath

