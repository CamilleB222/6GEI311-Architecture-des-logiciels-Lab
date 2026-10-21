from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from windowAcceuil import WindowAcceuil

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion de tickets")