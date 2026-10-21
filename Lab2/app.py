from windowAjoutImage import WindowAjoutImage
from windowAjoutTexte import WindowAjoutTexte
from windowConnect import WindowConnect
from windowAcceuil import WindowAcceuil
from windowCreeTicket import WindowCreeTicket
from windowListTicket import WindowListTicket
from PyQt6.QtWidgets import QApplication

def load_stylesheet(app, filename):
    with open(filename, "r", encoding="utf-8") as f:
        app.setStyleSheet(f.read())


app = QApplication([])
load_stylesheet(app, "style.qss")
window_connect = WindowCreeTicket()
window_connect.show()

app.exec()