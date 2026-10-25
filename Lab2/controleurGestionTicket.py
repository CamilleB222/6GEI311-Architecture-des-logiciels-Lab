from datetime import datetime
from pathlib import Path
import select
from tkinter import filedialog

from windowAssignation import WindowAssignation
from WindowVoirEditTicket import WindowVoirEditTicket
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
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from mainWindow import MainWindow
from breadcrumbPage import BreadcrumbPage
from statutTicket import StatutTicket


class ControleurGestionTicket:
    ticket_manager : TicketManager
    window_connect : WindowConnect
    window_acceuil : WindowAcceuil | None
    window_cree_ticket : WindowCreeTicket | None
    window_list_ticket : WindowListTicket | None
    window_ajout_texte : WindowAjoutTexte | None
    window_ajout_image : WindowAjoutImage | None
    window_voir_edit_ticket : WindowVoirEditTicket | None
    window_assignation : WindowAssignation | None
    _user_name : str | None
    _user_password : str | None
    _user_connected : User | None
    _list_user : list[User]
    _list_admin : list[Admin]
    _list_ticket : list[Ticket]
    _main_window : MainWindow | None
    _titre_ticket : str | None
    _titre_description : str
    _row_description : int
    _description_ini_ticket : str | None
    _description_ticket : str | None
    _priorité_ticket : str | None
    _list_description_ticket : DescriptionTicket | None
    _ajout_description : str | None
    _list_Description : list[DescriptionTicket]
    _ticket_edit : Ticket | None
    _ticket_edit_fermer_attente : bool
    _ticket_edit_status_attente : StatutTicket | None


    def __init__(self, list_user : list[User], list_admin : list[Admin], list_ticket : list[Ticket]):
        self._list_user = list_user
        self._list_admin = list_admin
        self._list_ticket = list_ticket

        self.ticket_manager = TicketManager(list_ticket, [*list_user, *list_admin])

        self.window_connect = WindowConnect()

        self.window_connect.textbox_nom.textChanged.connect(self.gerer_changement_texte_nom)
        self.window_connect.textbox_mdp.textChanged.connect(self.gerer_changement_texte_mdp)
        self.window_connect.button_connect.clicked.connect(self.gerer_clic_bouton_connexion)

        self.window_connect.show()

        self._user_name = None
        self._user_password = None
        self._user_connected = None
        self._main_window = None
        self.window_acceuil = None
        self.window_ajout_texte = None
        self.window_ajout_image = None
        self.window_assignation = None
        self.window_voir_edit_ticket = None
        self._titre_ticket = None
        self._titre_description = None
        self._row_description = -1
        self._description_ini_ticket = None
        self._description_ticket = None
        self._priorité_ticket = None
        self._list_Description = []
        self._ticket_edit = None
        self._ticket_edit_fermer_attente = False
        self._ticket_edit_status_attente = None

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

        self._main_window.adjustSize()


    def gerer_window_acceuil(self):
        self.window_acceuil = WindowAcceuil(self._user_connected.name, self._user_connected.role, isinstance(self._user_connected, Admin))

        self.window_acceuil.btn_create_ticket.clicked.connect(self.gerer_clic_bouton_creer_ticket)
        self.window_acceuil.btn_list_ticket.clicked.connect(self.gerer_clic_bouton_liste_ticket)
        self.window_acceuil.btn_disconect.clicked.connect(self.gerer_clic_bouton_deconnexion)

        self.gerer_main_window(self.window_acceuil)


    def gerer_clic_bouton_creer_ticket(self):
        widget_actuel = self._main_window.centralWidget()
        self._titre_ticket = ""
        self._description_ini_ticket = ""
        self._priorité_ticket = ""
        self._list_Description.clear()
        if isinstance(widget_actuel, WindowAcceuil):
            self.gerer_window_cree_ticket(self._user_connected.name, self._user_connected.role, [(BreadcrumbPage.Accueil,"Accueil"), (BreadcrumbPage.CreeTicket,"Créer ticket")])
        else:
            self.gerer_window_cree_ticket(self._user_connected.name, self._user_connected.role, [(BreadcrumbPage.Accueil,"Accueil"), (BreadcrumbPage.ListTicket, "Liste ticket"), (BreadcrumbPage.CreeTicket,"Créer ticket")])

    def gerer_clic_bouton_liste_ticket(self):
        if self._user_connected.role == "admin":
            self.gerer_window_list_ticket(self._user_connected.name, self._user_connected.role, [(BreadcrumbPage.Accueil,"Accueil"), (BreadcrumbPage.CreeTicket,"Liste ticket")], self._list_ticket)
        else:
            self.gerer_window_list_ticket(self._user_connected.name, self._user_connected.role, [(BreadcrumbPage.Accueil,"Accueil"), (BreadcrumbPage.CreeTicket,"Liste ticket")], self._user_connected.asign_tickets)

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

    def gerer_window_cree_ticket(self, nom : str, role : str, breadcrumbs : list[tuple[BreadcrumbPage, str]]):
        self.window_cree_ticket = WindowCreeTicket(nom, role, breadcrumbs)

        self.window_cree_ticket.textbox_titre_ticket.setText(self._titre_ticket)
        self.window_cree_ticket.textbox_description_ticket.setPlainText(self._description_ini_ticket)
        self.window_cree_ticket.textbox_priorite_ticket.setText(self._priorité_ticket)

        self.window_cree_ticket.header.breadcrumb_clicked.connect(self.gerer_clic_breadcrumb)
        self.window_cree_ticket.btn_creer_ticket.setEnabled(False)

        self.window_cree_ticket.textbox_titre_ticket.textChanged.connect(self.gerer_changement_texte_creer)
        self.window_cree_ticket.textbox_description_ticket.textChanged.connect(self.gerer_changement_texte_creer)
        self.window_cree_ticket.textbox_priorite_ticket.textChanged.connect(self.gerer_changement_texte_creer)

        self.window_cree_ticket.ajouter_descrtion_texte.triggered.connect(self.gerer_ajouter_description_texte)
        self.window_cree_ticket.ajouter_description_image.triggered.connect(self.gerer_ajout_description_image)
        self.window_cree_ticket.btn_annuler.clicked.connect(lambda: self.gerer_clic_bouton_annuler(breadcrumbs[-2][1]))
        self.window_cree_ticket.btn_creer_ticket.clicked.connect(self.gerer_clic_bouton_creer)
        
        self.gerer_main_window(self.window_cree_ticket)

    def gerer_clic_breadcrumb(self, page : BreadcrumbPage):
        if page == BreadcrumbPage.Accueil:
            self.gerer_window_acceuil()
        elif page == BreadcrumbPage.ListTicket:
            self.gerer_window_list_ticket(self._user_connected.name, self._user_connected.role, [(BreadcrumbPage.Accueil,"Accueil"), (BreadcrumbPage.CreeTicket,"Liste ticket")], self._list_ticket)

    def gerer_changement_texte_creer(self):
        self._titre_ticket = self.window_cree_ticket.textbox_titre_ticket.text()
        self._description_ini_ticket = self.window_cree_ticket.textbox_description_ticket.toPlainText()
        self._priorité_ticket = self.window_cree_ticket.textbox_priorite_ticket.text()
        if self._titre_ticket and self._description_ini_ticket and self._priorité_ticket:
            self.window_cree_ticket.btn_creer_ticket.setEnabled(True)
        else:
            self.window_cree_ticket.btn_creer_ticket.setEnabled(False)

    def gerer_ajouter_description_texte(self):
        self.window_ajout_texte = WindowAjoutTexte()
        self._titre_description = ""
        self._description_ticket = ""
        self.window_ajout_texte.show()
        self.gerer_ajout_texte()

    def gerer_ajout_description_image(self):
        self.window_ajout_image = WindowAjoutImage()
        self._titre_description = ""
        self._description_ticket = ""
        self.window_ajout_image.show()
        self.gerer_ajout_image()

    def gerer_clic_bouton_annuler(self, ancienne_page : str):
        if ancienne_page == "Accueil":
            self.gerer_window_acceuil()
        elif ancienne_page == "Liste ticket":
            self.gerer_window_list_ticket(self._user_connected.name, self._user_connected.role, [(BreadcrumbPage.Accueil,"Accueil"), (BreadcrumbPage.CreeTicket,"Liste ticket")], self._list_ticket)

    def gerer_clic_bouton_creer(self):
        if not len(self._list_ticket) == 0:
            ticket_id = max(ticket.ticket_id for ticket in self._list_ticket) + 1
        else:
            ticket_id = 1

        ticket = Ticket(ticket_id, self._titre_ticket, self._description_ini_ticket, self._priorité_ticket, datetime.now(), datetime.now())
        for description in self._list_Description:
            if isinstance(description, DescriptionTicketTexte):
                ticket.add_description(DescriptionTicketTexte, description.get_titre(), description.get_description())
            else:
                ticket.add_description(DescriptionTicketImage, description.get_titre(), description.get_description())

        self.ticket_manager.creat_ticket(self._user_connected,ticket)

        self.window_cree_ticket.textbox_titre_ticket.clear()
        self._titre_ticket = ""
        self.window_cree_ticket.textbox_description_ticket.clear()
        self._description_ini_ticket = ""
        self.window_cree_ticket.textbox_priorite_ticket.clear()
        self._priorité_ticket = ""
        self._list_Description.clear()
        self.window_cree_ticket.remove_all_description()


    def gerer_ajout_texte(self):
        self.window_ajout_texte.textbox_titre.setText(self._titre_description)
        self.window_ajout_texte.description.setPlainText(self._description_ticket)

        self.window_ajout_texte.btn_ajouter.setEnabled(False)
        
        self.window_ajout_texte.textbox_titre.textChanged.connect(self.gerer_changement_champ_texte)
        self.window_ajout_texte.description.textChanged.connect(self.gerer_changement_champ_texte)

        self.window_ajout_texte.btn_annuler.clicked.connect(self.gerer_bouton_annuler_ajout)
        self.window_ajout_texte.btn_ajouter.clicked.connect(self.gerer_clic_bouton_ajout_text)

    def gerer_changement_champ_texte(self):
        self._titre_description = self.window_ajout_texte.textbox_titre.text()
        self._description_ticket = self.window_ajout_texte.description.toPlainText()
        if self._titre_description and self._description_ticket :
            self.window_ajout_texte.btn_ajouter.setEnabled(True)
        else:
            self.window_ajout_texte.btn_ajouter.setEnabled(False)

    def gerer_bouton_annuler_ajout(self):
        self._titre_description = ""
        self._description_ticket = ""
        self.window_ajout_texte = None
        self.window_ajout_image = None


    def gerer_clic_bouton_ajout_text(self):
        description_texte = DescriptionTicketTexte(self._titre_description, self._description_ticket)
        self._list_Description.append(description_texte)
        self.window_ajout_texte.close()
        self.window_ajout_texte = None

        if self.window_cree_ticket is not None:
            self.window_cree_ticket.add_description(description_texte, self.gerer_clic_bouton_modifie_description, self.gerer_clic_bouton_supprimer_description)
        
        self._titre_description = ""
        self._description_ticket = ""

    def gerer_ajout_image(self):
        self.window_ajout_image.textbox_titre.setText(self._titre_description)
        self.window_ajout_image.textbox_selection.setText(self._description_ticket)
        
        self.window_ajout_image.btn_ajouter.setEnabled(False)
        
        self.window_ajout_image.textbox_titre.textChanged.connect(self.gerer_changement_champ_image)
        self.window_ajout_image.textbox_selection.textChanged.connect(self.gerer_changement_champ_image)

        self.window_ajout_image.btn_selection.clicked.connect(self.gerer_bouton_selectionner)
        self.window_ajout_image.btn_annuler.clicked.connect(self.gerer_bouton_annuler_ajout)
        self.window_ajout_image.btn_ajouter.clicked.connect(self.gerer_clic_bouton_ajout_image)

    def gerer_changement_champ_image(self):
        self._titre_description = self.window_ajout_image.textbox_titre.text()
        self._description_ticket = self.window_ajout_image.textbox_selection.text()
        if self._titre_description and self._description_ticket :
            self.window_ajout_image.btn_ajouter.setEnabled(True)
        else:
            self.window_ajout_image.btn_ajouter.setEnabled(False)    
    
    def gerer_bouton_selectionner(self):
        self._description_ticket : str
        
        self._description_ticket = filedialog.askopenfilename(
            title = "Choisir une image",
            initialdir=Path.home
        )
        self.window_ajout_image.textbox_selection.setText(self._description_ticket)

        pixmap = QPixmap(self._description_ticket)
        pixmap_redim = pixmap.scaled(
            250,150,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.window_ajout_image.label_image_preview.setPixmap(pixmap_redim)
    
    def gerer_clic_bouton_ajout_image(self):
        description_image = DescriptionTicketImage(self._titre_description, self._description_ticket)
        self._list_Description.append(description_image)
        self.window_ajout_image.close()
        self.window_ajout_image = None

        if self.window_cree_ticket is not None:
            self.window_cree_ticket.add_description(description_image, self.gerer_clic_bouton_modifie_description, self.gerer_clic_bouton_supprimer_description)

        self._titre_description = ""
        self._description_ticket = ""

    def gerer_clic_bouton_modifie_description(self, row : int):
        # Ouvrir la page de création de description en mode modification
        description : DescriptionTicket = self._list_Description[row]
        if type(description) == DescriptionTicketTexte:
            #Ouvrir la fenêtre
            self.window_ajout_texte = WindowAjoutTexte()
            self.window_ajout_texte.show()

            #Modifier les bouton pour la modificaiton
            self.window_ajout_texte.textbox_titre.textChanged.connect(self.gerer_changement_champ_texte)
            self.window_ajout_texte.description.textChanged.connect(self.gerer_changement_champ_texte)
            self._row_description = row

            self.window_ajout_texte.textbox_titre.setText(description.get_titre())
            self.window_ajout_texte.description.setPlainText(description.get_description())

            self.window_ajout_texte.btn_ajouter.setText("Modifier")
            self.window_ajout_texte.labe_titre_page.setText("Modifier une description")

            self.window_ajout_texte.btn_annuler.clicked.connect(self.gerer_bouton_annuler_ajout)
            self.window_ajout_texte.btn_ajouter.clicked.connect(self.gerer_clic_bouton_modifier_text)
        else:
            self.window_ajout_image = WindowAjoutImage()
            self.window_ajout_image.show()

            self.window_ajout_image.textbox_titre.textChanged.connect(self.gerer_changement_champ_image)
            self.window_ajout_image.textbox_selection.textChanged.connect(self.gerer_changement_champ_image)

            self.window_ajout_image.textbox_titre.setText(description.get_titre())
            self.window_ajout_image.textbox_selection.setText(description.get_description())

            pixmap = QPixmap(self._description_ticket)
            pixmap_redim = pixmap.scaled(
                250,150,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.window_ajout_image.label_image_preview.setPixmap(pixmap_redim)

            self.window_ajout_image.btn_ajouter.setText("Modifier")
            self.window_ajout_image.label_titre_page.setText("Modifier une image")

            self.window_ajout_image.btn_selection.clicked.connect(self.gerer_bouton_selectionner)
            self.window_ajout_image.btn_annuler.clicked.connect(self.gerer_bouton_annuler_ajout)
            self.window_ajout_image.btn_ajouter.clicked.connect(self.gerer_clic_bouton_modifier_image)

    def gerer_clic_bouton_modifier_text(self):
        description_texte = DescriptionTicketTexte(self._titre_description, self._description_ticket)
        self._list_Description[self._row_description] = description_texte

        self.window_ajout_texte.close()
        self.window_ajout_texte = None

        if self.window_cree_ticket is not None:
            self.window_cree_ticket.edit_description(self._row_description,description_texte)
        
        self._titre_description = ""
        self._description_ticket = ""

    def gerer_clic_bouton_modifier_image(self):
            description_texte = DescriptionTicketImage(self._titre_description, self._description_ticket)
            self._list_Description[self._row_description] = description_texte
    
            self.window_ajout_image.close()
            self.window_ajout_image = None
    
            if self.window_cree_ticket is not None:
                self.window_cree_ticket.edit_description(self._row_description,description_texte)
            
            self._titre_description = ""
            self._description_ticket = ""

    def gerer_clic_bouton_supprimer_description(self, row : int):
        if self.window_cree_ticket is not None:
            self.window_cree_ticket.remove_description(row)

        del self._list_Description[row]
        pass
    
    def gerer_window_list_ticket(self, nom : str, role : str, breadcrumbs : list[tuple[BreadcrumbPage, str]], list_ticket : list [Ticket]):
        self.window_list_ticket = WindowListTicket(nom,role,isinstance(self._user_connected, Admin),breadcrumbs,list_ticket, self.gerer_clic_bouton_modifier, self.gerer_clic_bouton_supprimer)
        
        self.window_list_ticket.header_widget.breadcrumb_clicked.connect(self.gerer_clic_breadcrumb)
        self.window_list_ticket.btn_assign.clicked.connect(self.gerer_clic_bouton_assign_lot)
        self.window_list_ticket.btn_back.clicked.connect(lambda : self.gerer_clic_bouton_annuler(breadcrumbs[-2][1]))
        self.window_list_ticket.btn_create.clicked.connect(self.gerer_clic_bouton_creer_ticket)
        self.window_list_ticket.btn_delete.clicked.connect(self.gerer_clic_bouton_supprimer_lot)

        self.gerer_main_window(self.window_list_ticket)
    
    def gerer_clic_bouton_assign_lot(self):
        list_ticket : list[Ticket] = self.window_list_ticket.get_selected_tickets()

        if len(list_ticket) != 0:
            self.window_assignation = WindowAssignation(self.ticket_manager.list_user_assignable, list_ticket)
            self.window_assignation.show()
            self.window_assignation.btn_annuler.clicked.connect(self.gerer_clic_bouton_assign_annuler)
            self.window_assignation.btn_assigner.clicked.connect(self.gerer_clic_bouton_assign_assigner)

    def gerer_clic_bouton_assign_annuler(self):
        self.window_assignation.close()
        self.window_assignation = None

    def gerer_clic_bouton_assign_assigner(self):
        utilisateur_selectionner : User = self.window_assignation.get_selected_user()

        if utilisateur_selectionner != None:
            list_ticket = self.window_list_ticket.get_selected_tickets()
            for ticket in list_ticket:
                self.ticket_manager.assign_Ticket(self._user_connected, utilisateur_selectionner, ticket)
                self.window_list_ticket.change_user_assignement(utilisateur_selectionner.name)
            self.window_assignation.close()
            self.window_assignation = None

    def gerer_clic_bouton_supprimer_lot(self):
        ticket_a_supprimer : list[Ticket] = self.window_list_ticket.get_selected_tickets()
        self.window_list_ticket.remove_tickets(ticket_a_supprimer)
        for ticket in ticket_a_supprimer:
            self._list_ticket.remove(ticket)

    def gerer_clic_bouton_supprimer(self, row):
        if self.window_list_ticket is not None:
            self.window_list_ticket.remove_ticket(row)

        del self._list_ticket[row]

    def gerer_clic_bouton_modifier(self, row):
        ticket : Ticket
        if isinstance(self._user_connected,Admin):
            ticket = self._list_ticket[row]
        else:
            ticket = self._user_connected.asign_tickets[row]

        is_edit : bool = ticket.status != StatutTicket.FERMER
        is_admin : bool = isinstance(self._user_connected, Admin)

        self._ticket_edit = ticket
        self._list_Description = list(ticket.list_description)
        self._ticket_edit_fermer_attente = False
        self._ticket_edit_status_attente = ticket.status

        self._titre_ticket = self._ticket_edit.title
        self._description_ini_ticket = self._ticket_edit.description_ini
        self._priorité_ticket = self._ticket_edit.priority 

        if is_admin:
            self.window_voir_edit_ticket = WindowVoirEditTicket(ticket, is_edit, is_admin, self.gerer_clic_bouton_modifie_description_edit, self.gerer_clic_bouton_supprimer_description_edit)
        else:
            self.window_voir_edit_ticket = WindowVoirEditTicket(ticket, is_edit, is_admin, self.gerer_clic_bouton_modifie_description_edit, self.gerer_clic_bouton_supprimer_description_edit)
        self.window_voir_edit_ticket.show()
        self.window_voir_edit_ticket.btn_annuler.clicked.connect(self.gerer_clic_bouton_modifier_annuler)
        self.window_voir_edit_ticket.btn_modif_status.clicked.connect(self.gerer_clic_bouton_modifier_statut)
        if is_admin:
            self.window_voir_edit_ticket.btn_fermer_status.clicked.connect(self.gerer_clic_bouton_modifier_fermer_statut)
        self.window_voir_edit_ticket.ajouter_descrtion_texte.triggered.connect(self.gerer_ajouter_description_texte_edit)
        self.window_voir_edit_ticket.ajouter_description_image.triggered.connect(self.gerer_ajout_description_image_edit)
        self.window_voir_edit_ticket.btn_enregister_ticket.clicked.connect(self.gerer_clic_bouton_enregistrer)

        self.window_voir_edit_ticket.textbox_titre_ticket.textChanged.connect(self.gerer_changement_texte_modifier)
        self.window_voir_edit_ticket.textbox_description_ticket.textChanged.connect(self.gerer_changement_texte_modifier)
        self.window_voir_edit_ticket.textbox_priorite_ticket.textChanged.connect(self.gerer_changement_texte_modifier)

    def gerer_clic_bouton_modifier_statut(self):
        if self._ticket_edit_status_attente == StatutTicket.ASSIGNÉ:
            self._ticket_edit_status_attente = StatutTicket.VALIDATION
        elif self._ticket_edit_status_attente == StatutTicket.VALIDATION:
            self._ticket_edit_status_attente = StatutTicket.TERMINÉ
                

        self.window_voir_edit_ticket.label_status_ticket.setText(self._ticket_edit_status_attente.name)

    def gerer_clic_bouton_modifier_fermer_statut(self):
        self._ticket_edit_fermer_attente = True

        self.window_voir_edit_ticket.label_status_ticket.setText(StatutTicket.FERMER.name)

        self.window_voir_edit_ticket.stop_edit(isinstance(self._user_connected, Admin))
        self.window_voir_edit_ticket.btn_enregister_ticket.setEnabled(True)

    # Ajouter ou supprimer des description dans ajout modificaiton

    def gerer_clic_bouton_enregistrer(self):
        
        ticket = Ticket(self._ticket_edit.ticket_id, self._titre_ticket, self._description_ini_ticket, self._priorité_ticket, self._ticket_edit.creation_date, datetime.now(),self._ticket_edit_status_attente)
        for description in self._list_Description:
            if isinstance(description, DescriptionTicketTexte):
                ticket.add_description(DescriptionTicketTexte, description.get_titre(), description.get_description())
            else:
                ticket.add_description(DescriptionTicketImage, description.get_titre(), description.get_description())
        
        
        self.ticket_manager.update_ticket_complet(self._user_connected,self._ticket_edit, ticket)
    
        
        if self._ticket_edit_fermer_attente:
            self.ticket_manager.close_ticket(self._user_connected,ticket)

        self._titre_ticket = ""
        self._description_ini_ticket = ""
        self._priorité_ticket = ""
        self.window_voir_edit_ticket.close()
        self.window_voir_edit_ticket = None

        self.window_list_ticket.update_ticket(ticket)

    def gerer_changement_texte_modifier(self):
            self._titre_ticket = self.window_voir_edit_ticket.textbox_titre_ticket.text()
            self._description_ini_ticket = self.window_voir_edit_ticket.textbox_description_ticket.toPlainText()
            self._priorité_ticket = self.window_voir_edit_ticket.textbox_priorite_ticket.text()
            if self._titre_ticket and self._description_ini_ticket and self._priorité_ticket:
                self.window_voir_edit_ticket.btn_enregister_ticket.setEnabled(True)
            else:
                self.window_voir_edit_ticket.btn_enregister_ticket.setEnabled(False)

    def gerer_ajouter_description_texte_edit(self):
        self.window_ajout_texte = WindowAjoutTexte()
        self._titre_description = ""
        self._description_ticket = ""
        self.window_ajout_texte.show()
        self.gerer_ajout_texte_edit()
    
    def gerer_ajout_description_image_edit(self):
        self.window_ajout_image = WindowAjoutImage()
        self._titre_description = ""
        self._description_ticket = ""
        self.window_ajout_image.show()
        self.gerer_ajout_image_edit()

    def gerer_ajout_texte_edit(self):
        self.window_ajout_texte.textbox_titre.setText(self._titre_description)
        self.window_ajout_texte.description.setPlainText(self._description_ticket)

        self.window_ajout_texte.btn_ajouter.setEnabled(False)
        
        self.window_ajout_texte.textbox_titre.textChanged.connect(self.gerer_changement_champ_texte_edit)
        self.window_ajout_texte.description.textChanged.connect(self.gerer_changement_champ_texte_edit)

        self.window_ajout_texte.btn_annuler.clicked.connect(self.gerer_bouton_annuler_ajout_edit)
        self.window_ajout_texte.btn_ajouter.clicked.connect(self.gerer_clic_bouton_ajout_text_edit)

    def gerer_changement_champ_texte_edit(self):
        self._titre_description = self.window_ajout_texte.textbox_titre.text()
        self._description_ticket = self.window_ajout_texte.description.toPlainText()
        if self._titre_description and self._description_ticket :
            self.window_ajout_texte.btn_ajouter.setEnabled(True)
        else:
            self.window_ajout_texte.btn_ajouter.setEnabled(False)

    def gerer_bouton_annuler_ajout_edit(self):
        self._titre_description = ""
        self._description_ticket = ""
        self.window_ajout_texte = None
        self.window_ajout_image = None


    def gerer_clic_bouton_ajout_text_edit(self):
        description_texte = DescriptionTicketTexte(self._titre_description, self._description_ticket)
        self._list_Description.append(description_texte)
        self.window_ajout_texte.close()
        self.window_ajout_texte = None

        if self.window_voir_edit_ticket is not None:
            self.window_voir_edit_ticket.add_description(description_texte, self.gerer_clic_bouton_modifie_description_edit, self.gerer_clic_bouton_supprimer_description_edit)
        
        self._titre_description = ""
        self._description_ticket = ""

    def gerer_ajout_image_edit(self):
        self.window_ajout_image.textbox_titre.setText(self._titre_description)
        self.window_ajout_image.textbox_selection.setText(self._description_ticket)
        
        self.window_ajout_image.btn_ajouter.setEnabled(False)
        
        self.window_ajout_image.textbox_titre.textChanged.connect(self.gerer_changement_champ_image)
        self.window_ajout_image.textbox_selection.textChanged.connect(self.gerer_changement_champ_image)

        self.window_ajout_image.btn_selection.clicked.connect(self.gerer_bouton_selectionner)
        self.window_ajout_image.btn_annuler.clicked.connect(self.gerer_bouton_annuler_ajout_edit)
        self.window_ajout_image.btn_ajouter.clicked.connect(self.gerer_clic_bouton_ajout_image_edit)    
    
    def gerer_clic_bouton_ajout_image_edit(self):
        description_image = DescriptionTicketImage(self._titre_description, self._description_ticket)
        self._list_Description.append(description_image)
        self.window_ajout_image.close()
        self.window_ajout_image = None

        if self.window_voir_edit_ticket is not None:
            self.window_voir_edit_ticket.add_description(description_image, self.gerer_clic_bouton_modifie_description_edit, self.gerer_clic_bouton_supprimer_description_edit)

        self._titre_description = ""
        self._description_ticket = ""

    def gerer_clic_bouton_modifie_description_edit(self, row : int):
        # Ouvrir la page de création de description en mode modification
        description : DescriptionTicket = self._list_Description[row]
        if type(description) == DescriptionTicketTexte:
            #Ouvrir la fenêtre
            self.window_ajout_texte = WindowAjoutTexte()
            self.window_ajout_texte.show()

            #Modifier les bouton pour la modificaiton
            self.window_ajout_texte.textbox_titre.textChanged.connect(self.gerer_changement_champ_texte)
            self.window_ajout_texte.description.textChanged.connect(self.gerer_changement_champ_texte)
            self._row_description = row

            self.window_ajout_texte.textbox_titre.setText(description.get_titre())
            self.window_ajout_texte.description.setPlainText(description.get_description())

            self.window_ajout_texte.btn_ajouter.setText("Modifier")
            self.window_ajout_texte.labe_titre_page.setText("Modifier une description")

            self.window_ajout_texte.btn_annuler.clicked.connect(self.gerer_bouton_annuler_ajout)
            self.window_ajout_texte.btn_ajouter.clicked.connect(self.gerer_clic_bouton_modifier_text_edit)
        else:
            self.window_ajout_image = WindowAjoutImage()
            self.window_ajout_image.show()

            self.window_ajout_image.textbox_titre.textChanged.connect(self.gerer_changement_champ_image)
            self.window_ajout_image.textbox_selection.textChanged.connect(self.gerer_changement_champ_image)

            self.window_ajout_image.textbox_titre.setText(description.get_titre())
            self.window_ajout_image.textbox_selection.setText(description.get_description())

            pixmap = QPixmap(self._description_ticket)
            pixmap_redim = pixmap.scaled(
                250,150,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.window_ajout_image.label_image_preview.setPixmap(pixmap_redim)

            self.window_ajout_image.btn_ajouter.setText("Modifier")
            self.window_ajout_image.label_titre_page.setText("Modifier une image")

            self.window_ajout_image.btn_selection.clicked.connect(self.gerer_bouton_selectionner)
            self.window_ajout_image.btn_annuler.clicked.connect(self.gerer_bouton_annuler_ajout)
            self.window_ajout_image.btn_ajouter.clicked.connect(self.gerer_clic_bouton_modifier_image_edit)

    def gerer_clic_bouton_modifier_text_edit(self):
        description_texte = DescriptionTicketTexte(self._titre_description, self._description_ticket)
        self._list_Description[self._row_description] = description_texte

        self.window_ajout_texte.close()
        self.window_ajout_texte = None

        if self.window_voir_edit_ticket is not None:
            self.window_voir_edit_ticket.edit_description(self._row_description,description_texte)
        
        self._titre_description = ""
        self._description_ticket = ""

    def gerer_clic_bouton_modifier_image_edit(self):
            description_texte = DescriptionTicketImage(self._titre_description, self._description_ticket)
            self._list_Description[self._row_description] = description_texte
    
            self.window_ajout_image.close()
            self.window_ajout_image = None
    
            if self.window_voir_edit_ticket is not None:
                self.window_voir_edit_ticket.edit_description(self._row_description,description_texte)
            
            self._titre_description = ""
            self._description_ticket = ""

    def gerer_clic_bouton_supprimer_description_edit(self, row : int):
        if self.window_voir_edit_ticket is not None:
            self.window_voir_edit_ticket.remove_description(row)

        del self._list_Description[row]
        pass

    def gerer_clic_bouton_modifier_ticket(self):
        pass

    def gerer_clic_bouton_modifier_annuler(self):
        self._ticket_edit_fermer_attente = False
        self._ticket_edit_status_attente = None

        self.window_voir_edit_ticket.close()
        self.window_voir_edit_ticket = None
        

