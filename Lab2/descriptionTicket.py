from abc import ABC, abstractmethod

class DescriptionTicket(ABC):

    @abstractmethod
    def get_description(self):
        pass

