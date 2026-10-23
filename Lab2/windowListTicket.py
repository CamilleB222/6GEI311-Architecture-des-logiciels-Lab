from headerWidget import HeaderWidget
from PyQt6.QtWidgets import QCheckBox, QHBoxLayout, QLabel, QPushButton, QTableWidgetItem, QWidget, QHeaderView, QGridLayout,QTableWidget,QAbstractItemView
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QFont
from breadcrumbPage import BreadcrumbPage
from ticket import Ticket

class WindowListTicket(QWidget):
    def __init__(self, nom : str, role : str, breadcrumbs : list[tuple[BreadcrumbPage, str]], list_ticket : list[Ticket]):
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
            self.btn_layout.addWidget(self.btn_create)
            self.btn_layout.addWidget(self.btn_assign)
            self.btn_layout.addWidget(self.btn_delete)

            # 1. Création du tableau : 4 colonnes
            self.table = QTableWidget()
            self.table.setObjectName("ticketTable")
            self.table.setColumnCount(4)
            self.table.setHorizontalHeaderLabels(
                ["", "ID", "Titre", "Actions"]
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
                )  # Actions


            # 3. Remplissage du tableau
            self.table.setRowCount(len(list_ticket))
            for row, ticket in enumerate(list_ticket):
                # Col 0 : Checkbox pour multi-sélection
                chk_container = QWidget()
                chk_layout = QHBoxLayout(chk_container)
                chk_layout.addWidget(QCheckBox())
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

                # Col 3 : Actions avec pictogrammes/boutons
                actions_widget = self._create_actions_widget(ticket.ticket_id)
                self.table.setCellWidget(row, 3, actions_widget)


            self.layout_principal = QGridLayout()
            self.layout_principal.addWidget(self.header_widget, 0, 0)
            self.layout_principal.addWidget(self.table, 1,0)
            self.layout_principal.addLayout(self.btn_layout,2,0)

            self.layout_principal.setRowStretch(0,0)
            self.layout_principal.setRowStretch(1,1)

            self.setLayout(self.layout_principal)

    def _create_actions_widget(self, ticket_id):
        """Crée un conteneur horizontal avec des boutons d'actions pour la ligne."""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(4, 2, 4, 2)
        layout.setSpacing(6)
        
        # Bouton Édition / Voir
        btn_edit = QPushButton("✏️")  # Ou QIcon("path/to/edit.png")
        btn_edit.setObjectName("actionBtnEdit")
        btn_edit.setToolTip("Modifier")
        btn_edit.clicked.connect(
            lambda: print(f"Édition du ticket {ticket_id}")
        )

        # Bouton Suppression
        btn_delete = QPushButton("🗑️")  # Ou QIcon("path/to/delete.png")
        btn_delete.setObjectName("actionBtnDelete")
        btn_delete.setToolTip("Supprimer")
        btn_delete.clicked.connect(
            lambda: print(f"Suppression du ticket {ticket_id}")
        )

        layout.addWidget(btn_edit)
        layout.addWidget(btn_delete)
        return container