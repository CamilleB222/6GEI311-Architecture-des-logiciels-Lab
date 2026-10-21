from headerWidget import HeaderWidget
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QHeaderView, QLabel, QMenu, QPlainTextEdit, QPushButton, QTableWidget, QVBoxLayout, QWidget, QLineEdit, QGridLayout
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction, QFont

class WindowAjoutTexte(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestionnaire de tickets")
        self.setFixedSize(500,300)

        labe_titre_page = QLabel("Ajouter une description", self)

        description = QPlainTextEdit(self)

        btn_annuler = QPushButton("Annuler", self)
        btn_ajouter = QPushButton("Ajouter", self)

        layout_btn = QHBoxLayout()
        layout_btn.addWidget(btn_annuler, alignment=Qt.AlignmentFlag.AlignLeft)
        layout_btn.addWidget(btn_ajouter, alignment=Qt.AlignmentFlag.AlignRight)

        layout_principal = QVBoxLayout()
        layout_principal.addWidget(labe_titre_page, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_principal.addWidget(description)
        layout_principal.addLayout(layout_btn)

        self.setLayout(layout_principal)