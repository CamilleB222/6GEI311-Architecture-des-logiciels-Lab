from abc import ABC, abstractmethod

class DescriptionTicket(ABC):

    @abstractmethod
    def get_titre(self) -> str:
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        pass

