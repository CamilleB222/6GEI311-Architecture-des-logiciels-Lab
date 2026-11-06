from abc import ABC, abstractmethod

class DescriptionTicket(ABC):
    _id : int

    def __init__(self, id : int | None = None) -> None:
        super().__init__()
        self._id = id

    @property
    def id(self) -> int | None:
        return self._id

    @abstractmethod
    def get_titre(self) -> str:
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        pass

