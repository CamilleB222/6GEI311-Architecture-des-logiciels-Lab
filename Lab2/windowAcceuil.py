from headerWidget import HeaderWidget
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit, QGridLayout
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QFont

class WindowAcceuil(QWidget):
    def __init__(self, nom : str, role : str):
            super().__init__()
            self.setWindowTitle("Gestionnaire de tickets")
            self.setFixedSize(500,300)

            header = HeaderWidget("Bienvenu Xavier", "Admin")
            btn_layout = QGridLayout()

            btn_create_ticket = QPushButton("Créer ticket")
            btn_create_ticket.setProperty("class", "btnAcc")
            btn_list_ticket = QPushButton("Liste tickets")
            btn_list_ticket.setProperty("class", "btnAcc")
            btn_disconect = QPushButton("Déconnexion")
            btn_disconect.setProperty("class", "btnAcc")

            btn_layout.addWidget(btn_create_ticket,0,0, alignment=Qt.AlignmentFlag.AlignCenter)
            btn_layout.addWidget(btn_list_ticket,0,1, alignment=Qt.AlignmentFlag.AlignCenter)
            btn_layout.addWidget(btn_disconect,1,0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)

            layout_principal = QGridLayout()
            layout_principal.addWidget(header, 0, 0)
            layout_principal.addLayout(btn_layout,1,0)

            layout_principal.setRowStretch(0,0)
            layout_principal.setRowStretch(1,1)

            self.setLayout(layout_principal)