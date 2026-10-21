from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit
from PyQt6.QtCore import Qt

class WindowAjoutImage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestionnaire de tickets")
        self.setFixedSize(500,300)

        self.labe_titre_page = QLabel("Ajouter une image", self)

        self.btn_selection = QPushButton("Sélectionner", self)
        self.textbox_selection = QLineEdit(self)

        self.label_image_preview = QLabel("Aperçu de l'image", self)

        self.btn_annuler = QPushButton("Annuler", self)
        self.btn_ajouter = QPushButton("Ajouter", self)

        self.layout_selection = QHBoxLayout()
        self.layout_selection.addWidget(self.btn_selection, alignment=Qt.AlignmentFlag.AlignLeft)
        self.layout_selection.addWidget(self.textbox_selection)
        
        self.layout_btn = QHBoxLayout()
        self.layout_btn.addWidget(self.btn_annuler, alignment=Qt.AlignmentFlag.AlignLeft)
        self.layout_btn.addWidget(self.btn_ajouter, alignment=Qt.AlignmentFlag.AlignRight)

        self.layout_principal = QVBoxLayout()
        self.layout_principal.addWidget(self.labe_titre_page, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout_principal.addLayout(self.layout_selection)
        self.layout_principal.addWidget(self.label_image_preview, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout_principal.addLayout(self.layout_btn)

        self.setLayout(self.layout_principal)
