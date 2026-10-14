from windowConnect import WindowConnect
from windowAcceuil import WindowAcceuil
from windowListTicket import WindowListTicket
from PyQt6.QtWidgets import QApplication

def load_stylesheet(app, filename):
    with open(filename, "r", encoding="utf-8") as f:
        app.setStyleSheet(f.read())


app = QApplication([])
load_stylesheet(app, "style.qss")
window_connect = WindowListTicket()
window_connect.show()

app.exec()