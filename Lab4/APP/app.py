import os
import sys
dossier_app = os.path.dirname(os.path.abspath(__file__))
if dossier_app not in sys.path:
  sys.path.insert(0, dossier_app)

from datetime import datetime

from controleurGestionTicket import ControleurGestionTicket
from PyQt6.QtWidgets import QApplication

app : QApplication
controleur : ControleurGestionTicket


def load_stylesheet(app, filename):
    with open(filename, "r", encoding="utf-8") as f:
        app.setStyleSheet(f.read())

def main():
    
    app = QApplication([])
    dir_path = os.path.dirname(os.path.realpath(__file__))
    load_stylesheet(app,  dir_path + "/style.qss")

    controleur = ControleurGestionTicket()
    app.exec()


if __name__ == "__main__":
    main()