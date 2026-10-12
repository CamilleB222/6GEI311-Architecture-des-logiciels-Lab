from PyQt6.QtWidgets import QApplication, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit, QGridLayout
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QFont

class WindowConnect(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestionnaire de tickets")
        self.setFixedSize(400,200)
        
        label_titre = QLabel("Connexion", self)
        label_titre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_titre.setStyleSheet("font-size: 30px; font-weight: bold; margin-bottom: 20px;")

        grid = QGridLayout()

        font_info = QFont("Arial", 15)
        
        label_nom = QLabel("Nom d'utilisateur : ", self)
        label_nom.setFont(font_info)

        textbox_nom = QLineEdit(self)
        textbox_nom.setFont(font_info)

        label_mdp = QLabel("Mot de passe : ", self)
        label_mdp.setFont(font_info)

        textbox_mdp = QLineEdit(self)
        textbox_mdp.setFont(font_info)

        grid.addWidget(label_nom, 0, 0, alignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
        grid.addWidget(textbox_nom, 0, 1, alignment=Qt.AlignmentFlag.AlignVCenter)

        grid.addWidget(label_mdp, 1, 0, alignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
        grid.addWidget(textbox_mdp, 1, 1, alignment=Qt.AlignmentFlag.AlignVCenter)

        button_connect = QPushButton("Connexion", self)

        layout_principal = QVBoxLayout()
        layout_principal.addWidget(label_titre, 0)
        layout_principal.addLayout(grid)
        layout_principal.addWidget(button_connect)

        self.setLayout(layout_principal)