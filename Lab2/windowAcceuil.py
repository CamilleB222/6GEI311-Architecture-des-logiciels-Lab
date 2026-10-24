from headerWidget import HeaderWidget
from PyQt6.QtWidgets import QPushButton, QWidget, QGridLayout
from PyQt6.QtCore import Qt

class WindowAcceuil(QWidget):
    def __init__(self, nom : str, role : str, is_admin : bool):
            super().__init__()
            self.setWindowTitle("Gestionnaire de tickets")
            self.setFixedSize(500,300)

            self.header = HeaderWidget(f"Bienvenu {nom}", role)
            self.btn_layout = QGridLayout()

            self.btn_create_ticket = QPushButton("Créer ticket")
            self.btn_create_ticket.setProperty("class", "btnAcc")
            self.btn_list_ticket = QPushButton("Liste tickets")
            self.btn_list_ticket.setProperty("class", "btnAcc")
            self.btn_disconect = QPushButton("Déconnexion")
            self.btn_disconect.setProperty("class", "btnAcc")



            if is_admin:
                self.btn_layout.addWidget(self.btn_create_ticket,0,0, alignment=Qt.AlignmentFlag.AlignCenter)
                self.btn_layout.addWidget(self.btn_list_ticket,0,1, alignment=Qt.AlignmentFlag.AlignCenter)
            else:
                self.btn_layout.addWidget(self.btn_list_ticket,0,0,1,2,alignment=Qt.AlignmentFlag.AlignCenter)

            self.btn_layout.addWidget(self.btn_disconect,1,0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)

            self.layout_principal = QGridLayout()
            self.layout_principal.addWidget(self.header, 0, 0)
            self.layout_principal.addLayout(self.btn_layout,1,0)

            self.layout_principal.setRowStretch(0,0)
            self.layout_principal.setRowStretch(1,1)

            self.setLayout(self.layout_principal)