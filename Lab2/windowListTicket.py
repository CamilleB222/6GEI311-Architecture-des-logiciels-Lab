from headerWidget import HeaderWidget
from PyQt6.QtWidgets import QCheckBox, QHBoxLayout, QLabel, QPushButton, QTableWidgetItem, QWidget, QHeaderView, QGridLayout,QTableWidget,QAbstractItemView
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QFont
from breadcrumbPage import BreadcrumbPage
from ticket import Ticket
from typing import Callable

class WindowListTicket(QWidget):
    def __init__(self, nom : str, role : str, is_admin : bool ,breadcrumbs : list[tuple[BreadcrumbPage, str]], list_ticket : list[Ticket], edit: Callable[[int], None], delete: Callable[[int], None]):
            super().__init__()
            self.setWindowTitle("Gestionnaire de tickets")
            self.setFixedSize(700,400)

            self.header_widget = HeaderWidget(nom, role)
            self.header_widget.set_breadcrumbs(breadcrumbs)

            self.titre_label = QLabel("Liste dees tickets")
            self.titre_label.setObjectName("listTicketTitle")
            
            self.btn_layout = QHBoxLayout()

            self.btn_back = QPushButton("Retour")
            self.btn_back.setProperty("class", "btnListTicket")
            self.btn_create = QPushButton("Créer")
            self.btn_create.setProperty("class", "btnListTicket")
            self.btn_assign = QPushButton("Assigner")
            self.btn_assign.setProperty("class", "btnListTicket")
            self.btn_delete = QPushButton("Supprimer")
            self.btn_delete.setProperty("class", "btnListTicket")

            self.btn_layout.addWidget(self.btn_back)
            self.btn_layout.addStretch()

            if is_admin:
                self.btn_layout.addWidget(self.btn_create)
                self.btn_layout.addWidget(self.btn_assign)
                self.btn_layout.addWidget(self.btn_delete)

            # 1. Création du tableau : 5 colonnes
            self.table = QTableWidget()
            self.table.setObjectName("ticketTable")
            self.table.setColumnCount(5)
            self.table.setHorizontalHeaderLabels(
                ["", "ID", "Titre", "Utilisateur" ,"Actions"]
            )

            # Configuration du comportement de la grille
            self.table.setSelectionBehavior(
                QAbstractItemView.SelectionBehavior.SelectRows
            )
            self.table.setSelectionMode(
                QAbstractItemView.SelectionMode.NoSelection
            )

            self.table.setAlternatingRowColors(True)

            # 2. Gestion des largeurs de colonnes
            header = self.table.horizontalHeader()

            if header is not None:
                header.setSectionResizeMode(
                    0, QHeaderView.ResizeMode.ResizeToContents
                )  # Multi-sélection
                header.setSectionResizeMode(
                    1, QHeaderView.ResizeMode.ResizeToContents
                )  # ID
                header.setSectionResizeMode(
                    2, QHeaderView.ResizeMode.Stretch
                )  # Titre
                header.setSectionResizeMode(
                    3, QHeaderView.ResizeMode.ResizeToContents
                )  # utilisateur assigné
                header.setSectionResizeMode(
                    4, QHeaderView.ResizeMode.ResizeToContents
                )  # Actions


            # 3. Remplissage du tableau
            self.table.setRowCount(len(list_ticket))
            for row, ticket in enumerate(list_ticket):
                # Col 0 : Checkbox pour multi-sélection
                chk_container = QWidget()
                chk_layout = QHBoxLayout(chk_container)
                checkbox = QCheckBox()
                # Rattachement de l'objet ticket (ou de ticket.ticket_id)
                checkbox.setProperty("ticket", ticket)
                chk_layout.addWidget(checkbox)
                chk_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
                chk_layout.setContentsMargins(0, 0, 0, 0)
                self.table.setCellWidget(row, 0, chk_container)

                # Col 1 : ID
                item_id = QTableWidgetItem(str(ticket.ticket_id))
                item_id.setFlags(
                    item_id.flags() ^ Qt.ItemFlag.ItemIsEditable
                )
                item_id.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, 1, item_id)

                # Col 2 : Titre
                item_title = QTableWidgetItem(ticket.title)
                item_title.setFlags(
                    item_title.flags() ^ Qt.ItemFlag.ItemIsEditable
                )
                self.table.setItem(row, 2, item_title)

                # Col 3 : Utilisatuer asigné
                item_assign = QTableWidgetItem(str(ticket.user_assign or "Aucun"))
                item_assign.setFlags(
                    item_assign.flags() ^ Qt.ItemFlag.ItemIsEditable
                )
                item_assign.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, 3, item_assign)

                # Col 4 : Actions avec pictogrammes/boutons
                actions_widget = self._create_actions_widget(ticket.ticket_id, edit, delete)
                self.table.setCellWidget(row, 4, actions_widget)


            self.layout_principal = QGridLayout()
            self.layout_principal.addWidget(self.header_widget, 0, 0)
            self.layout_principal.addWidget(self.table, 1,0)
            self.layout_principal.addLayout(self.btn_layout,2,0)

            self.layout_principal.setRowStretch(0,0)
            self.layout_principal.setRowStretch(1,1)

            self.setLayout(self.layout_principal)

    def remove_ticket(self, row):
             self.table.removeRow(row)

    def remove_tickets(self, tickets_to_remove: list[Ticket]) -> None:
        # Extraction des IDs pour gérer indifféremment des objets Ticket ou des entiers
        ids_to_remove = { t.ticket_id for t in tickets_to_remove}

        for row in range(self.table.rowCount() - 1, -1, -1):
            container = self.table.cellWidget(row, 0)
            if container:
                checkbox = container.findChild(QCheckBox)
                if checkbox:
                    ticket = checkbox.property("ticket")
                    
                    if ticket.ticket_id in ids_to_remove:
                        self.table.removeRow(row)

    def get_selected_tickets(self) -> list[Ticket]:
        """Retourne la liste des objets Ticket dont la case est cochée."""
        selected_tickets = []
        
        for row in range(self.table.rowCount()):
            container = self.table.cellWidget(row, 0)
            if container:
                checkbox = container.findChild(QCheckBox)
                if checkbox and checkbox.isChecked():
                    ticket = checkbox.property("ticket")
                    if ticket:
                        selected_tickets.append(ticket)
                        
        return selected_tickets

    def get_selected_ticket_ids(self) -> list[int]:
        """Variante : Retourne uniquement la liste des IDs des tickets cochés."""
        return [ticket.ticket_id for ticket in self.get_selected_tickets()]

    def _get_current_row(self, widget: QWidget) -> int:
        """Retrouve la ligne courante d'un widget imbriqué dans la table."""
        # Convertit la position relative du widget en coordonnées globales de la table
        pos = widget.parentWidget().mapTo(self.table.viewport(), widget.pos())
        index = self.table.indexAt(pos)
        return index.row() if index.isValid() else -1

    def _create_actions_widget(self, is_admin : bool, edit: Callable[[int], None], delete: Callable[[int], None]):
        """Crée un conteneur horizontal avec des boutons d'actions pour la ligne."""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(4, 2, 4, 2)
        layout.setSpacing(6)
        
        # Bouton Édition / Voir
        btn_edit = QPushButton("👁️/✏️")  # Ou QIcon("path/to/edit.png")
        btn_edit.setObjectName("actionBtnEdit")
        btn_edit.setToolTip("Modifier")
        btn_edit.clicked.connect(
            lambda _, b=btn_edit: self._handle_action(b, edit)
        )

        layout.addWidget(btn_edit)

        if is_admin:
            # Bouton Suppression
            btn_delete = QPushButton("🗑️")  # Ou QIcon("path/to/delete.png")
            btn_delete.setObjectName("actionBtnDelete")
            btn_delete.setToolTip("Supprimer")
            btn_delete.clicked.connect(
                lambda _, b=btn_delete: self._handle_action(b, delete)
            )
            layout.addWidget(btn_delete)


        return container
    
    def _handle_action(self, button: QPushButton, callback: Callable[[int], None]):
        """Exécute le callback avec l'index de ligne calculé à la volée."""
        current_row = self._get_current_row(button)
        if current_row != -1:
            callback(current_row)