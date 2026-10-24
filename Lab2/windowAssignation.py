from PyQt6.QtWidgets import QAbstractItemView, QCheckBox, QHBoxLayout, QHeaderView, QLabel, QMenu, QPlainTextEdit, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QLineEdit, QGridLayout
from PyQt6.QtCore import Qt
from user import User

class WindowAssignation(QWidget):
    def __init__(self, list_user : list[User]):
        super().__init__()
        self.setWindowTitle("Gestionnaire de tickets")
        self.setFixedSize(500,300)

        self.label_titre_page = QLabel("Assignation de ticket(s)", self)
        self.label_titre_page.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_titre_page.setStyleSheet("font-size: 30px; font-weight: bold; margin-bottom: 20px;")

        self.label_ticket = QLabel("Ticket(s) : ", self)
        self.label_list_ticket = QLabel("", self)

        self.btn_annuler = QPushButton("Annuler", self)
        self.btn_assigner = QPushButton("Assigner", self)

        self.table = QTableWidget(self)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Sélection", "Employé"])
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.table.setAlternatingRowColors(True)
        self.table_heander = self.table.horizontalHeader()
        self.table_heander.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table_heander.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

        #Rmplissage tableau
        self.table.setRowCount(len(list_user))
        for row, user in enumerate(list_user):
            nom = user.name
            #col 0
            chk_container = QWidget()
            chk_layout = QHBoxLayout(chk_container)
            chk_layout.addWidget(QCheckBox())
            chk_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            chk_layout.setContentsMargins(0, 0, 0, 0)
            self.table.setCellWidget(row, 0, chk_container)

            #col 1
            nom_user = QTableWidgetItem(str(nom))
            nom_user.setFlags(nom_user.flags() ^Qt.ItemFlag.ItemIsEditable)
            nom_user.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            self.table.setItem(row,1,nom_user)

        self.layout_ticket = QHBoxLayout()
        self.layout_ticket.addWidget(self.label_ticket, alignment=Qt.AlignmentFlag.AlignLeft)
        self.layout_ticket.addWidget(self.label_list_ticket)

        self.layout_btn = QHBoxLayout()
        self.layout_btn.addWidget(self.btn_annuler, alignment=Qt.AlignmentFlag.AlignLeft)
        self.layout_btn.addWidget(self.btn_assigner, alignment=Qt.AlignmentFlag.AlignRight)

        self.layout_principal = QVBoxLayout()
        self.layout_principal.addWidget(self.label_titre_page)
        self.layout_principal.addLayout(self.layout_ticket)
        self.layout_principal.addWidget(self.table)
        self.layout_principal.addLayout(self.layout_btn)

        self.setLayout(self.layout_principal)
