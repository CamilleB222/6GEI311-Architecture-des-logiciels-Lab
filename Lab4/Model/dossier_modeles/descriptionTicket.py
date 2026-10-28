from abc import ABC, abstractmethod
from pydantic import BaseModel

class DescriptionTicket(BaseModel, ABC):

    @abstractmethod
    def get_titre(self):
        pass
    
    @abstractmethod
    def get_description(self):
        pass

