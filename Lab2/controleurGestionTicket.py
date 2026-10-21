from windowAcceuil import WindowAcceuil
from windowCreeTicket import WindowCreeTicket
from windowListTicket import WindowListTicket
from windowAjoutTexte import WindowAjoutTexte
from windowAjoutImage import WindowAjoutImage
from windowConnect import WindowConnect
from admin import Admin
from user import User
from ticket import Ticket
from ticketManager import TicketManager
from descriptionTicket import DescriptionTicket
from descriptionTicketImage import DescriptionTicketImage
from descriptionTicketTexte import DescriptionTicketTexte
from PyQt6.QtWidgets import QMessageBox, QWidget
from mainWindow import MainWindow


class ControleurGestionTicket:
    ticket_manager : TicketManager
    window_connect : WindowConnect
    window_acceuil : WindowAcceuil | None
    window_cree_ticket : WindowCreeTicket | None
    window_list_ticket : WindowListTicket | None
    window_ajout_texte : WindowAjoutTexte | None
    window_ajout_image : WindowAjoutImage | None
    _user_name : str | None
    _user_password : str | None
    _user_connected : User | None
    _list_user : list[User]
    _list_admin : list[Admin]
    _list_ticket : list[Ticket]
    _main_window : MainWindow | None

    def __init__(self, list_user : list[User], list_admin : list[Admin], list_ticket : list[Ticket]):
        self._list_user = list_user
        self._list_admin = list_admin
        self._list_ticket = list_ticket

        self.ticket_manager = TicketManager()

        self.window_connect = WindowConnect()

        self.window_connect.textbox_nom.textChanged.connect(self.gerer_changement_texte_nom)
        self.window_connect.textbox_mdp.textChanged.connect(self.gerer_changement_texte_mdp)
        self.window_connect.button_connect.clicked.connect(self.gerer_clic_bouton_connexion)

        self.window_connect.show()

        self._user_name = None
        self._user_password = None
        self._user_connected = None
        self._main_window = None

    def gerer_changement_texte_nom(self):
        self._user_name = self.window_connect.textbox_nom.text()

    def gerer_changement_texte_mdp(self):
        self._user_password = self.window_connect.textbox_mdp.text()
        if self._user_name and self._user_password:
            self.window_connect.button_connect.setEnabled(True)
        else:
            self.window_connect.button_connect.setEnabled(False)

    def gerer_clic_bouton_connexion(self):
        user_connected = None
        for user in self._list_user:
            if user.name == self._user_name and not self._user_password == "":
                user_connected = user
                break

        if not user_connected:
            for admin in self._list_admin:
                if admin.name == self._user_name and not self._user_password == "":
                    user_connected = admin
                    break

        if not user_connected:
            QMessageBox.warning(self.window_connect, "Erreur de connexion", "Nom d'utilisateur ou mot de passe incorrect.")
            return

        self._user_connected = user_connected
        self.window_connect.close()

        self.gerer_window_acceuil()

    def gerer_main_window(self, prochaine_fenetre : QWidget):
        if self._main_window is None:
            self._main_window = MainWindow()
            self._main_window.show()

        self._main_window.setCentralWidget(prochaine_fenetre)


    def gerer_window_acceuil(self):
        self.window_acceuil = WindowAcceuil(self._user_connected.name, self._user_connected.role)

        self.window_acceuil.btn_create_ticket.clicked.connect(self.gerer_clic_bouton_creer_ticket)
        self.window_acceuil.btn_list_ticket.clicked.connect(self.gerer_clic_bouton_liste_ticket)
        self.window_acceuil.btn_disconect.clicked.connect(self.gerer_clic_bouton_deconnexion)

        self.gerer_main_window(self.window_acceuil)


    def gerer_clic_bouton_creer_ticket(self):
        pass

    def gerer_clic_bouton_liste_ticket(self):
        pass

    def gerer_clic_bouton_deconnexion(self):
        self._main_window.close()
        self._user_connected = None
        self.window_acceuil = None
        self.window_cree_ticket = None
        self.window_list_ticket = None
        self._main_window = None

        self.window_connect.textbox_nom.clear()
        self.window_connect.textbox_mdp.clear()
        self.window_connect.button_connect.setEnabled(False)
        self.window_connect.show()


        

