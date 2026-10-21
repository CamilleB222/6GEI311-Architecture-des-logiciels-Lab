from headerWidget import HeaderWidget
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QHeaderView, QLabel, QMenu, QPlainTextEdit, QPushButton, QTableWidget, QVBoxLayout, QWidget, QLineEdit, QGridLayout
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction, QFont

class WindowAjoutImage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestionnaire de tickets")
        self.setFixedSize(500,300)

        labe_titre_page = QLabel("Ajouter une image", self)

        btn_selection = QPushButton("Sélectionner", self)
        textbox_selection = QLineEdit(self)

        label_image_preview = QLabel("Aperçu de l'image", self)

        btn_annuler = QPushButton("Annuler", self)
        btn_ajouter = QPushButton("Ajouter", self)

        layout_selection = QHBoxLayout()
        layout_selection.addWidget(btn_selection, alignment=Qt.AlignmentFlag.AlignLeft)
        layout_selection.addWidget(textbox_selection)
        
        layout_btn = QHBoxLayout()
        layout_btn.addWidget(btn_annuler, alignment=Qt.AlignmentFlag.AlignLeft)
        layout_btn.addWidget(btn_ajouter, alignment=Qt.AlignmentFlag.AlignRight)

        layout_principal = QVBoxLayout()
        layout_principal.addWidget(labe_titre_page, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_principal.addLayout(layout_selection)
        layout_principal.addWidget(label_image_preview, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_principal.addLayout(layout_btn)

        self.setLayout(layout_principal)
