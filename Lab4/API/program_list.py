from dossier_modeles import Admin, Ticket, User
from services.ticketManager import TicketManager

list_user : list[User] = list[User]()
list_admin : list[Admin] = list[Admin]()
list_tickets : list[Ticket] = list[Ticket]()

ticket_manager : TicketManager = TicketManager(list_tickets, list_user)