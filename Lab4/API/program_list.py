from dossier_modeles import Admin, Ticket, User
from services.ticketManager import TicketManager

list_user : list[User] = list[User]()
list_admin : list[Admin] = list[Admin]()
list_tickets : list[Ticket] = list[Ticket]()

dict_user_connect : dict[str, User] = dict[str, User]()
max_description_id: int = 0

def generer_nouvel_id() -> int:
    global max_description_id
    max_description_id += 1
    return max_description_id

ticket_manager : TicketManager = TicketManager(list_tickets, list_user)