from headerWidget import HeaderWidget
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QHeaderView, QLabel, QMenu, QPlainTextEdit, QPushButton, QTableWidget, QVBoxLayout, QWidget, QLineEdit, QGridLayout
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction, QFont

from windowAjoutImage import WindowAjoutImage
from windowAjoutTexte import WindowAjoutTexte

class WindowCreeTicket(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestionnaire de tickets")
        self.setFixedSize(500,500)

        header = HeaderWidget("Camille", "Admin")
        label_titre_page = QLabel("Création d'un ticket", self)
        label_titre_page.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_titre_page.setStyleSheet("font-size: 30px; font-weight: bold; margin-bottom: 20px;")

        label_titre_ticket = QLabel("Titre du ticket : ", self)
        label_description_ticket = QLabel("Description du ticket : ", self)
        label_priorite_ticket = QLabel("Priorité du ticket : ", self)

        textbox_titre_ticket = QLineEdit(self)
        textbox_description_ticket = QPlainTextEdit(self)
        textbox_priorite_ticket = QLineEdit(self)

        btn_ajouter_description = QPushButton("Ajouter description", self)
        menu = QMenu(self)
        ajouter_descrtion_texte = QAction("Ajouter une description", self)
        ajouter_description_image = QAction("Ajouter une image", self)
        menu.addAction(ajouter_descrtion_texte)
        menu.addAction(ajouter_description_image)
        btn_ajouter_description.setMenu(menu)

        self.table = QTableWidget(self)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Description", "Type", "Action"])
        table_heander = self.table.horizontalHeader()
        table_heander.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        table_heander.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        table_heander.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.table.setRowCount(0)

        btn_annuler = QPushButton("Annuler", self)
        btn_creer_ticket = QPushButton("Créer", self)

        grid_description = QGridLayout()
        grid_description.addWidget(label_titre_ticket, 0, 0, alignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
        grid_description.addWidget(textbox_titre_ticket, 0, 1, alignment=Qt.AlignmentFlag.AlignVCenter)
        grid_description.addWidget(label_description_ticket, 1, 0, alignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
        grid_description.addWidget(textbox_description_ticket, 1, 1, alignment=Qt.AlignmentFlag.AlignVCenter)
        grid_description.addWidget(label_priorite_ticket, 2, 0, alignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
        grid_description.addWidget(textbox_priorite_ticket, 2, 1, alignment=Qt.AlignmentFlag.AlignVCenter)

        grid_btn = QGridLayout()
        grid_btn.addWidget(btn_annuler, 0, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        grid_btn.addWidget(btn_creer_ticket, 0, 1, alignment=Qt.AlignmentFlag.AlignRight)

        layout_principal = QVBoxLayout()
        layout_principal.addWidget(header)
        layout_principal.addWidget(label_titre_page)
        layout_principal.addLayout(grid_description)
        layout_principal.addWidget(btn_ajouter_description)
        layout_principal.addWidget(self.table)
        layout_principal.addLayout(grid_btn)

        self.setLayout(layout_principal)

