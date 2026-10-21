from headerWidget import HeaderWidget
from breadcrumbPage import BreadcrumbPage
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QHeaderView, QLabel, QMenu, QPlainTextEdit, QPushButton, QTableWidget, QVBoxLayout, QWidget, QLineEdit, QGridLayout
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction, QFont

from windowAjoutImage import WindowAjoutImage
from windowAjoutTexte import WindowAjoutTexte

class WindowCreeTicket(QWidget):
    def __init__(self, nom : str, role : str, breadcrumbs : list[tuple[BreadcrumbPage, str]]):
        super().__init__()
        self.setWindowTitle("Gestionnaire de tickets")
        self.setFixedSize(500,500)

        self.header = HeaderWidget(nom, role)
        self.header.set_breadcrumbs(breadcrumbs)

        self.label_titre_page = QLabel("Création d'un ticket", self)
        self.label_titre_page.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_titre_page.setStyleSheet("font-size: 30px; font-weight: bold; margin-bottom: 20px;")

        self.label_titre_ticket = QLabel("Titre du ticket : ", self)
        self.label_description_ticket = QLabel("Description du ticket : ", self)
        self.label_priorite_ticket = QLabel("Priorité du ticket : ", self)

        self.textbox_titre_ticket = QLineEdit(self)
        self.textbox_description_ticket = QPlainTextEdit(self)
        self.textbox_priorite_ticket = QLineEdit(self)

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
        self.table.setHorizontalHeaderLabels(["Description", "Type", "Action"])
        self.table_heander = self.table.horizontalHeader()
        self.table_heander.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table_heander.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table_heander.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.table.setRowCount(0)

        self.btn_annuler = QPushButton("Annuler", self)
        self.btn_annuler.setProperty("class", "btnListTicket")
        self.btn_creer_ticket = QPushButton("Créer", self)
        self.btn_creer_ticket.setProperty("class", "btnListTicket")

        self.grid_description = QGridLayout()
        self.grid_description.addWidget(self.label_titre_ticket, 0, 0, alignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
        self.grid_description.addWidget(self.textbox_titre_ticket, 0, 1, alignment=Qt.AlignmentFlag.AlignVCenter)
        self.grid_description.addWidget(self.label_description_ticket, 1, 0, alignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
        self.grid_description.addWidget(self.textbox_description_ticket, 1, 1, alignment=Qt.AlignmentFlag.AlignVCenter)
        self.grid_description.addWidget(self.label_priorite_ticket, 2, 0, alignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
        self.grid_description.addWidget(self.textbox_priorite_ticket, 2, 1, alignment=Qt.AlignmentFlag.AlignVCenter)

        self.grid_btn = QGridLayout()
        self.grid_btn.addWidget(self.btn_annuler, 0, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        self.grid_btn.addWidget(self.btn_creer_ticket, 0, 1, alignment=Qt.AlignmentFlag.AlignRight)

        self.layout_principal = QVBoxLayout()
        self.layout_principal.addWidget(self.header)
        self.layout_principal.addWidget(self.label_titre_page)
        self.layout_principal.addLayout(self.grid_description)
        self.layout_principal.addWidget(self.btn_ajouter_description)
        self.layout_principal.addWidget(self.table)
        self.layout_principal.addLayout(self.grid_btn)

        self.setLayout(self.layout_principal)

