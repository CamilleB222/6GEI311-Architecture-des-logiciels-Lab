from headerWidget import HeaderWidget
from PyQt6.QtWidgets import QCheckBox, QHBoxLayout, QLabel, QPushButton, QTableWidgetItem, QWidget, QHeaderView, QGridLayout,QTableWidget,QAbstractItemView
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QFont
from breadcrumbPage import BreadcrumbPage

class WindowListTicket(QWidget):
    def __init__(self, nom : str, role : str, breadcrumbs : list[tuple[BreadcrumbPage, str]]):
            super().__init__()
            self.setWindowTitle("Gestionnaire de tickets")
            self.setFixedSize(700,400)

            header_widget = HeaderWidget("Xavier", "Admin")
            header_widget.set_breadcrumbs(breadcrumbs)

            titre_label = QLabel("Liste dees tickets")
            titre_label.setObjectName("listTicketTitle")
            
            btn_layout = QHBoxLayout()

            btn_back = QPushButton("Retour")
            btn_back.setProperty("class", "btnListTicket")
            btn_create = QPushButton("Créer")
            btn_create.setProperty("class", "btnListTicket")
            btn_assign = QPushButton("Assigner")
            btn_assign.setProperty("class", "btnListTicket")
            btn_delete = QPushButton("Supprimer")
            btn_delete.setProperty("class", "btnListTicket")

            btn_layout.addWidget(btn_back)
            btn_layout.addStretch()
            btn_layout.addWidget(btn_create)
            btn_layout.addWidget(btn_assign)
            btn_layout.addWidget(btn_delete)

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
                )  # Multi-sélection (Ajusté)
                header.setSectionResizeMode(
                    1, QHeaderView.ResizeMode.ResizeToContents
                )  # ID (Ajusté)
                header.setSectionResizeMode(
                    2, QHeaderView.ResizeMode.Stretch
                )  # Titre (Prend tout l'espace)
                header.setSectionResizeMode(
                    3, QHeaderView.ResizeMode.ResizeToContents
                )  # Actions (Ajusté)

            # Données de test
            tickets = [
                (101, "Erreur d'accès à la base de données"),
                (102, "Problème d'impression bureau 3"),
                (103, "Mise à jour du pare-feu requise"),
            ]

            # 3. Remplissage du tableau
            self.table.setRowCount(len(tickets))
            for row, (ticket_id, title) in enumerate(tickets):
                # Col 0 : Checkbox pour multi-sélection
                chk_container = QWidget()
                chk_layout = QHBoxLayout(chk_container)
                chk_layout.addWidget(QCheckBox())
                chk_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
                chk_layout.setContentsMargins(0, 0, 0, 0)
                self.table.setCellWidget(row, 0, chk_container)

                # Col 1 : ID (Non éditable)
                item_id = QTableWidgetItem(str(ticket_id))
                item_id.setFlags(
                    item_id.flags() ^ Qt.ItemFlag.ItemIsEditable
                )
                item_id.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, 1, item_id)

                # Col 2 : Titre
                item_title = QTableWidgetItem(title)
                item_title.setFlags(
                    item_title.flags() ^ Qt.ItemFlag.ItemIsEditable
                )
                self.table.setItem(row, 2, item_title)

                # Col 3 : Actions avec pictogrammes/boutons
                actions_widget = self._create_actions_widget(ticket_id)
                self.table.setCellWidget(row, 3, actions_widget)


            layout_principal = QGridLayout()
            layout_principal.addWidget(header_widget, 0, 0)
            layout_principal.addWidget(self.table, 1,0)
            layout_principal.addLayout(btn_layout,2,0)

            layout_principal.setRowStretch(0,0)
            layout_principal.setRowStretch(1,1)

            self.setLayout(layout_principal)

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