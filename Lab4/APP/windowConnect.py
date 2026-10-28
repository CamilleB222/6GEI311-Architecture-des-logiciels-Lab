from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit, QGridLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class WindowConnect(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestionnaire de tickets")
        self.setFixedSize(400,200)
        
        label_titre = QLabel("Connexion", self)
        label_titre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_titre.setStyleSheet("font-size: 30px; font-weight: bold; margin-bottom: 20px;")

        self.grid = QGridLayout()

        font_info = QFont("Arial", 15)
        
        self.label_nom = QLabel("Nom d'utilisateur : ", self)
        self.label_nom.setFont(font_info)

        self.textbox_nom = QLineEdit(self)
        self.textbox_nom.setFont(font_info)

        self.label_mdp = QLabel("Mot de passe : ", self)
        self.label_mdp.setFont(font_info)

        self.textbox_mdp = QLineEdit(self)
        self.textbox_mdp.setFont(font_info)

        self.grid.addWidget(self.label_nom, 0, 0, alignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
        self.grid.addWidget(self.textbox_nom, 0, 1, alignment=Qt.AlignmentFlag.AlignVCenter)

        self.grid.addWidget(self.label_mdp, 1, 0, alignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
        self.grid.addWidget(self.textbox_mdp, 1, 1, alignment=Qt.AlignmentFlag.AlignVCenter)

        self.button_connect = QPushButton("Connexion", self)
        self.button_connect.setEnabled(False)

        layout_principal = QVBoxLayout()
        layout_principal.addWidget(label_titre, 0)
        layout_principal.addLayout(self.grid)
        layout_principal.addWidget(self.button_connect)

        self.setLayout(layout_principal)