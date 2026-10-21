from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPlainTextEdit, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt

class WindowAjoutTexte(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestionnaire de tickets")
        self.setFixedSize(500,300)

        self.labe_titre_page = QLabel("Ajouter une description", self)

        self.description = QPlainTextEdit(self)

        self.btn_annuler = QPushButton("Annuler", self)
        self.btn_ajouter = QPushButton("Ajouter", self)

        self.layout_btn = QHBoxLayout()
        self.layout_btn.addWidget(self.btn_annuler, alignment=Qt.AlignmentFlag.AlignLeft)
        self.layout_btn.addWidget(self.btn_ajouter, alignment=Qt.AlignmentFlag.AlignRight)

        self.layout_principal = QVBoxLayout()
        self.layout_principal.addWidget(self.labe_titre_page, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout_principal.addWidget(self.description)
        self.layout_principal.addLayout(self.layout_btn)

        self.setLayout(self.layout_principal)