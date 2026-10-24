from datetime import datetime

from controleurGestionTicket import ControleurGestionTicket
from admin import Admin
from ticket import Ticket
from ticketManager import TicketManager
from user import User
from windowAjoutImage import WindowAjoutImage
from windowAjoutTexte import WindowAjoutTexte
from windowConnect import WindowConnect
from windowAcceuil import WindowAcceuil
from windowCreeTicket import WindowCreeTicket
from windowListTicket import WindowListTicket
from PyQt6.QtWidgets import QApplication
import os

app : QApplication
controleur : ControleurGestionTicket

list_user : list[User] = list[User]()
list_admin : list[Admin] = list[Admin]()
list_tickets : list[Ticket] = list[Ticket]()

def load_stylesheet(app, filename):
    with open(filename, "r", encoding="utf-8") as f:
        app.setStyleSheet(f.read())

def register_user(user : User):
    if isinstance(user, Admin):
        if user not in list_admin:
            list_admin.append(user)
    else:
        if user not in list_user:
            list_user.append(user)

def main():
    admin1 = Admin(1, 'c', 'cbarrette@etu.uqac.ca')
    register_user(admin1)
    user1 = User(1,'x','xtremblay@etu.uqac.ca', 'développeur')
    user2 = User(2, 'Zachary Harvey', 'zharvey@etu.uqac.ca', 'apprenti')
    register_user(user1)
    register_user(user2)

    #Pour les test
    list_tickets.append(Ticket(1,"c","c","c",datetime.now(), datetime.now()))
    list_tickets.append(Ticket(2,"c1","c1","c1",datetime.now(), datetime.now()))
    list_tickets.append(Ticket(3,"c2","c2","c2",datetime.now(), datetime.now()))
    list_tickets.append(Ticket(4,"c3","c3","c3",datetime.now(), datetime.now()))
    list_tickets.append(Ticket(5,"c4","c4","c4",datetime.now(), datetime.now()))

    app = QApplication([])
    dir_path = os.path.dirname(os.path.realpath(__file__))
    load_stylesheet(app,  dir_path + "/style.qss")

    controleur = ControleurGestionTicket(list_user, list_admin, list_tickets)
    app.exec()


if __name__ == "__main__":
    main()