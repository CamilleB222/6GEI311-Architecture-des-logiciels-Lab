from descriptionTicketTexte import DescriptionTicketTexte
from PyQt6.QtWidgets import QAbstractItemView, QHBoxLayout, QHeaderView, QLabel, QMenu, QPlainTextEdit, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QLineEdit, QGridLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from statutTicket import StatutTicket
from ticket import Ticket
from typing import Callable
from descriptionTicket import DescriptionTicket

class WindowVoirEditTicket(QWidget):
    def __init__(self, ticket : Ticket,is_edit : bool, is_admin : bool, edit:Callable[[int],None], delete:Callable[[int], None]):
        super().__init__()
        self.setWindowTitle("Gestionnaire de tickets")
        self.setFixedSize(500,500)

        self.label_titre_page = QLabel("Lecture/Edition d'un ticket", self)
        self.label_titre_page.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_titre_page.setStyleSheet("font-size: 30px; font-weight: bold; margin-bottom: 20px;")

        self.label_titre_ticket = QLabel("Titre du ticket : ", self)
        self.label_description_ticket = QLabel("Description du ticket : ", self)
        self.label_priorite_ticket = QLabel("Priorité du ticket : ", self)
        self.label_status = QLabel("Status : ", self)
        self.label_status_ticket = QLabel(ticket.status.name, self)
        self.btn_modif_status = QPushButton("Modifier", self)
        self.btn_modif_status.setEnabled(ticket.status != StatutTicket.OUVERT and ticket.status != StatutTicket.TERMINÉ)

        if is_admin:
            self.btn_fermer_status = QPushButton("Fermer", self)

        self.label_date_creation = QLabel("Date de crétion : ",self)
        self.label_date_creation_ticket = QLabel(ticket.creation_date.strftime("%Y-%m-%d %H:%M:%S"), self)
        self.label_date_modif = QLabel("Date de modification : ", self)
        self.label_date_modif_ticket = QLabel(ticket.update_date.strftime("%Y-%m-%d %H:%M:%S"), self)
        

        self.textbox_titre_ticket = QLineEdit(self)
        self.textbox_titre_ticket.setText(ticket.title)
        self.textbox_description_ticket = QPlainTextEdit(self)
        self.textbox_description_ticket.setPlainText(ticket.description_ini)
        self.textbox_priorite_ticket = QLineEdit(self)
        self.textbox_priorite_ticket.setText(ticket.priority)


        self.btn_ajouter_description = QPushButton("Ajouter description", self)
        self.menu = QMenu(self)
        self.ajouter_descrtion_texte = QAction("Ajouter une description", self)
        self.ajouter_description_image = QAction("Ajouter une image", self)
        self.menu.addAction(self.ajouter_descrtion_texte)
        self.menu.addAction(self.ajouter_description_image)
        self.btn_ajouter_description.setMenu(self.menu)

        self.table = QTableWidget(self)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Titre description", "Type", "Action"])
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.table.setAlternatingRowColors(True)
        self.table_heander = self.table.horizontalHeader()
        self.table_heander.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table_heander.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table_heander.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        #Remplissage tableau
        self.table.setRowCount(len(ticket.list_description))
        for row, description in enumerate(ticket.list_description):
            titre = description.get_titre()
            #col 0
            titre_description = QTableWidgetItem(str(titre))
            titre_description.setFlags(titre_description.flags() ^ Qt.ItemFlag.ItemIsEditable)
            titre_description.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            self.table.setItem(row,0,titre_description)
            #col 1 : type
            if isinstance(description, DescriptionTicketTexte):
                type_description = QTableWidgetItem(str("Texte"))
            else:
                type_description = QTableWidgetItem(str("Image"))
            type_description.setFlags(type_description.flags() ^ Qt.ItemFlag.ItemIsEditable)
            type_description.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row,1,type_description)
            #col 2 : Actions
            actions_widget = self._create_actions_widget(edit,delete)
            self.table.setCellWidget(row, 2, actions_widget)

        self.btn_annuler = QPushButton("Annuler", self)
        self.btn_annuler.setProperty("class", "btnListTicket")
        self.btn_enregister_ticket = QPushButton("Enregistrer", self)
        self.btn_enregister_ticket.setProperty("class", "btnListTicket")

        self.grid_description = QGridLayout()
        self.grid_description.addWidget(self.label_titre_ticket, 0, 0, alignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
        self.grid_description.addWidget(self.textbox_titre_ticket, 0, 1, alignment=Qt.AlignmentFlag.AlignVCenter)
        self.grid_description.addWidget(self.label_description_ticket, 1, 0, alignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
        self.grid_description.addWidget(self.textbox_description_ticket, 1, 1, alignment=Qt.AlignmentFlag.AlignVCenter)
        self.grid_description.addWidget(self.label_priorite_ticket, 2, 0, alignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
        self.grid_description.addWidget(self.textbox_priorite_ticket, 2, 1, alignment=Qt.AlignmentFlag.AlignVCenter)
        self.grid_description.addWidget(self.label_status,3,0,alignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
        self.grid_description.addWidget(self.label_status_ticket,3,1,alignment=Qt.AlignmentFlag.AlignVCenter)
        self.grid_description.addWidget(self.btn_modif_status,3,2)

        if is_admin:
            self.grid_description.addWidget(self.btn_fermer_status,3,3)
        self.grid_description.addWidget(self.label_date_creation,4,0,alignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
        self.grid_description.addWidget(self.label_date_creation_ticket,4,1,alignment=Qt.AlignmentFlag.AlignVCenter)
        self.grid_description.addWidget(self.label_date_modif,5,0,alignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
        self.grid_description.addWidget(self.label_date_modif_ticket,5,1,alignment=Qt.AlignmentFlag.AlignVCenter)

        self.grid_btn = QGridLayout()
        self.grid_btn.addWidget(self.btn_annuler, 0, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        self.grid_btn.addWidget(self.btn_enregister_ticket, 0, 1, alignment=Qt.AlignmentFlag.AlignRight)

        self.layout_principal = QVBoxLayout()
        self.layout_principal.addWidget(self.label_titre_page)
        self.layout_principal.addLayout(self.grid_description)
        self.layout_principal.addWidget(self.btn_ajouter_description)
        self.layout_principal.addWidget(self.table)
        self.layout_principal.addLayout(self.grid_btn)

        self.setLayout(self.layout_principal)

        if not is_edit:
             self.stop_edit(is_admin)


    def stop_edit(self, is_admin : bool):
        self.btn_modif_status.setEnabled(False)
        self.btn_enregister_ticket.setEnabled(False)
        if is_admin:
            self.btn_fermer_status.setEnabled(False)
        self.textbox_priorite_ticket.setEnabled(False)
        self.textbox_titre_ticket.setEnabled(False)
        self.textbox_description_ticket.setEnabled(False)
        self.btn_ajouter_description.setEnabled(False)

    def add_description(self, description : DescriptionTicket, edit : Callable[[int], None], delete : Callable[[int], None]):
        row = self.table.rowCount()
        self.table.setRowCount(row + 1)
        titre = description.get_titre()

        #col 0
        titre_description = QTableWidgetItem(str(titre))
        titre_description.setFlags(titre_description.flags() ^ Qt.ItemFlag.ItemIsEditable)
        titre_description.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.table.setItem(row,0,titre_description)

        #col 1 : type
        if isinstance(description, DescriptionTicketTexte):
            type_description = QTableWidgetItem(str("Texte"))
        else:
            type_description = QTableWidgetItem(str("Image"))

        type_description.setFlags(type_description.flags() ^ Qt.ItemFlag.ItemIsEditable)
        type_description.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        self.table.setItem(row,1,type_description)

        #col 2 : Actions
        actions_widget = self._create_actions_widget(edit, delete)
        self.table.setCellWidget(row, 2, actions_widget)

    def edit_description(self, row: int, description: DescriptionTicket):
        """Met à jour le titre et le type d'une ligne existante."""
        if 0 <= row < self.table.rowCount():
            # Col 0 : Mise à jour du titre
            self.table.item(row, 0).setText(str(description.get_titre()))
            
            # Col 1 : Mise à jour du type
            type_str = "Texte" if isinstance(description, DescriptionTicketTexte) else "Image"
            self.table.item(row, 1).setText(type_str)

    def remove_description(self, row):
         self.table.removeRow(row)

    def remove_all_description(self):
        self.table.setRowCount(0)

    def _get_current_row(self, widget: QWidget) -> int:
        """Retrouve la ligne courante d'un widget imbriqué dans la table."""
        # Convertit la position relative du widget en coordonnées globales de la table
        pos = widget.parentWidget().mapTo(self.table.viewport(), widget.pos())
        index = self.table.indexAt(pos)
        return index.row() if index.isValid() else -1
         

    def _create_actions_widget(self, edit: Callable[[int], None], delete: Callable[[int], None]):
            """Crée un conteneur horizontal avec des boutons d'actions pour la ligne."""
            container = QWidget()
            layout = QHBoxLayout(container)
            layout.setContentsMargins(4, 2, 4, 2)
            layout.setSpacing(6)

            # Bouton Édition
            btn_edit = QPushButton("✏️")
            btn_edit.setObjectName("actionBtnEdit")
            btn_edit.setToolTip("Modifier")
            btn_edit.clicked.connect(
                lambda _, b=btn_edit: self._handle_action(b, edit)
            )

            # Bouton Suppression
            btn_delete = QPushButton("🗑️")
            btn_delete.setObjectName("actionBtnDelete")
            btn_delete.setToolTip("Supprimer")
            btn_delete.clicked.connect(
                lambda _, b=btn_delete: self._handle_action(b, delete)
            )

            layout.addWidget(btn_edit)
            layout.addWidget(btn_delete)
            return container

    
    def _handle_action(self, button: QPushButton, callback: Callable[[int], None]):
        """Exécute le callback avec l'index de ligne calculé à la volée."""
        current_row = self._get_current_row(button)
        if current_row != -1:
            callback(current_row)
    
    