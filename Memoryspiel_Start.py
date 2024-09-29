from PyQt5.QtWidgets import QApplication
from spieldaten.memoryspiel import Memoryspiel
                   
app = QApplication([])
fenster = Memoryspiel()

app.exec()
