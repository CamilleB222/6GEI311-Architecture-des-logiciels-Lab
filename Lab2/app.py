from windowAjoutImage import WindowAjoutImage
from windowAjoutTexte import WindowAjoutTexte
from windowConnect import WindowConnect
from windowAcceuil import WindowAcceuil
<<<<<<< HEAD
from windowCreeTicket import WindowCreeTicket
=======
from windowListTicket import WindowListTicket
>>>>>>> aea48257750091f285a7031d5e368ca740c23fa0
from PyQt6.QtWidgets import QApplication

def load_stylesheet(app, filename):
    with open(filename, "r", encoding="utf-8") as f:
        app.setStyleSheet(f.read())


app = QApplication([])
load_stylesheet(app, "style.qss")
<<<<<<< HEAD
window_connect = WindowCreeTicket()
=======
window_connect = WindowListTicket()
>>>>>>> aea48257750091f285a7031d5e368ca740c23fa0
window_connect.show()

app.exec()