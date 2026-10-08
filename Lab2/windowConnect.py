from PyQt6.QtWidgets import QApplication, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QFont

class WindowConnect(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestionnaire de tickets")
        
        label_titre = QLabel("Page de connexion", self)
        label_titre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_titre.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        label_nom = QLabel("Nom d'utilisateur : ", self)
        label_nom.setFont(QFont("Arial", 12))
        label_nom.setAlignment(Qt.AlignmentFlag.AlignRight)
        textbox_nom = QLineEdit(self)
        label_mdp = QLabel("Mot de passe : ", self)
        label_mdp.setFont(QFont("Arial", 12))
        label_mdp.setAlignment(Qt.AlignmentFlag.AlignRight)
        textbox_mdp = QLineEdit(self)
        button_connect = QPushButton("Connexion", self)

        layout_nom = QHBoxLayout()
        layout_nom.addWidget(label_nom, 10)
        layout_nom.addWidget(textbox_nom)

        layout_mdp = QHBoxLayout()
        layout_mdp.addWidget(label_mdp,10)
        layout_mdp.addWidget(textbox_mdp)

        layout_principal = QVBoxLayout()
        layout_principal.addWidget(label_titre)
        layout_principal.addLayout(layout_nom)
        layout_principal.addLayout(layout_mdp)
        layout_principal.addWidget(button_connect)

        self.setLayout(layout_principal)