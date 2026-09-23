from enum import Enum

class StatutTicket(Enum):
    OUVERT = 0
    ASSIGNÉ = 1
    VALIDATION = 2
    TERMINÉ = 3
    FERMER = 4