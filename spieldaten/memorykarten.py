from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtGui import QIcon

class Memorykarte (QTableWidgetItem):
    def __init__(self, vorne, nummer):
        super().__init__()
        self.bild_vorne = QIcon(vorne)
        self.bild_hinten = QIcon("bilder/back.bmp")
        self.setIcon(self.bild_hinten)

        self.umgedreht = False
        self.noch_im_spiel = True
        self.bild_ID = nummer
        self.bild_pos = 0

    def umdrehen(self):
        if self.noch_im_spiel == True:
            if self.umgedreht == True:
                self.setIcon(self.bild_hinten)
                self.umgedreht = False
            else:
                self.setIcon(self.bild_vorne)
                self.umgedreht = True

    def rausnehmen(self):
        self.setIcon(QIcon("bilder/aufgedeckt.bmp"))
        self.noch_im_spiel = False

    def get_bild_ID(self):
        return self.bild_ID

    def get_bild_pos(self):
        return self.bild_pos

    def set_bild_pos(self, position):
        self.bild_pos = position

    def get_noch_im_spiel(self):
        return self.noch_im_spiel

    def get_umgedreht(self):
        return self.umgedreht

