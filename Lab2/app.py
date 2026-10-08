from windowConnect import WindowConnect
from PyQt6.QtWidgets import QApplication

app = QApplication([])
window_connect = WindowConnect()
window_connect.show()

app.exec()