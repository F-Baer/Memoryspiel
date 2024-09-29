from PyQt5.QtWidgets import QWidget, QTableWidget, QAbstractItemView, QLabel, QMessageBox, QPushButton, QGroupBox, QRadioButton, QHBoxLayout
from PyQt5.QtCore import QSize, QTimer

import random
from spieldaten import memorykarten


class Memoryspiel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Memoryspiel")
        self.setFixedSize(395, 575)
        
        #Spiel-Variablen
        self.timer_umdrehen = QTimer(self)
        self.timer_umdrehen.setSingleShot(True)
        self.umgedrehte_karten = 0
        self.spieler = 0
        self.mensch_punkte = 0
        self.computer_punkte = 0
        self.gemerkte_karten = [[-1] * 21 for index in range(2)]
        self.paar = [None, None] 
        self.spielstaerke = 10
        
        #Spielfeld initialiseiren
        self.spielfeld = QTableWidget(7, 6, self)      
        self.spielfeld.horizontalHeader().hide()
        self.spielfeld.verticalHeader().hide()
        self.spielfeld.setShowGrid(False)
        self.spielfeld.setSelectionMode(QTableWidget.NoSelection)
        self.spielfeld.setEditTriggers(QAbstractItemView.NoEditTriggers)
                    
        zeilen = range(0, 7)
        spalten = range(0, 6)

        for zeile in zeilen:
            self.spielfeld.setRowHeight(zeile, 66)
        for spalte in spalten:
            self.spielfeld.setColumnWidth(spalte, 64)
            
        self.spielfeld.cellClicked.connect(self.maus_klick_slot)
        self.timer_umdrehen.timeout.connect(self.timer_slot)
        
        self.spielfeld.resize(386, 464)

        # Labels für die Anzeigen
        self.label_text_mensch = QLabel(self)
        self.label_text_mensch.setText("Mensch")
        self.label_text_mensch.setGeometry(10, 475, 60, 25)
        self.label_mensch = QLabel(self)
        self.label_mensch.setText("0")
        self.label_mensch.setGeometry(80, 475, 60, 25)

        self.label_text_computer = QLabel(self)
        self.label_text_computer.setText("Computer")
        self.label_text_computer.setGeometry(10, 495, 60, 25)
        self.label_computer = QLabel(self)
        self.label_computer.setText("0")
        self.label_computer.setGeometry(80, 495, 60, 25)
        
        self.label_aktueller_spieler = QLabel(self)
        self.label_aktueller_spieler.setText("Es zieht der")
        self.label_aktueller_spieler.setGeometry(10, 530, 60, 25)
        self.label_aktueller_spieler_anzeigen = QLabel(self)
        self.label_aktueller_spieler_anzeigen.setText("Mensch")
        self.label_aktueller_spieler_anzeigen.setGeometry(80, 530, 60, 25)

        self.schummeln_button = QPushButton(self)
        self.schummeln_button.setGeometry(310, 530, 70, 36)
        self.schummeln_button.setText("Schummeln")
        
        self.schummeln_button.clicked.connect(self.schummeln)
        
        self.schummeln_timer = QTimer(self)
        self.schummeln_timer.setSingleShot(True)
        self.schummeln_timer.timeout.connect(self.schummeln_vorbei)
        
        # Groupbox Layout Spielstärke 
        self.spielstaerke_box = QGroupBox("Spielstärke", self)
        self.spielstaerke_box.setGeometry(130, 475, 250, 46)
        spielstaerke_layout = QHBoxLayout()
        
        self.spielstaerke_leicht = QRadioButton("Leicht")
        self.spielstaerke_mittel = QRadioButton("Mittel")            
        self.spielstaerke_schwer = QRadioButton("Schwer")
        self.spielstaerke_extrem = QRadioButton("Extrem")
                
        spielstaerke_layout.addWidget(self.spielstaerke_leicht)
        spielstaerke_layout.addWidget(self.spielstaerke_mittel)
        spielstaerke_layout.addWidget(self.spielstaerke_schwer)
        spielstaerke_layout.addWidget(self.spielstaerke_extrem)
        self.spielstaerke_box.setLayout(spielstaerke_layout)
        
        self.spielstaerke_mittel.setChecked(True)
        
        # Spielstärken auswahl
        self.spielstaerke_leicht.toggled.connect(lambda: self.set_spielstaerke(20))
        self.spielstaerke_mittel.toggled.connect(lambda: self.set_spielstaerke(10))
        self.spielstaerke_schwer.toggled.connect(lambda: self.set_spielstaerke(4))
        self.spielstaerke_extrem.toggled.connect(lambda: self.set_spielstaerke(1))
        
        # Groupbox Spieler Wahl
        self.spieler_wahl_box = QGroupBox(self)
        self.spieler_wahl_box.setGeometry(130, 530, 180, 35)
        spieler_wahl_layout = QHBoxLayout()
        
        self.vs_mensch = QRadioButton("VS Mensch")
        self.vs_computer = QRadioButton("VS Computer")
        
        spieler_wahl_layout.addWidget(self.vs_mensch)
        spieler_wahl_layout.addWidget(self.vs_computer)
        self.spieler_wahl_box.setLayout(spieler_wahl_layout)
        
        self.vs_computer.setChecked(True)

        self.bild_namen = [
            "bilder/apfel.bmp", "bilder/birne.bmp",
            "bilder/blume.bmp", "bilder/blume2.bmp",
            "bilder/ente.bmp", "bilder/fisch.bmp",
            "bilder/fuchs.bmp", "bilder/igel.bmp",
            "bilder/kaenguruh.bmp", "bilder/katze.bmp",
            "bilder/kuh.bmp", "bilder/maus1.bmp",
            "bilder/maus2.bmp", "bilder/maus3.bmp",
            "bilder/melone.bmp", "bilder/pilz.bmp",
            "bilder/ronny.bmp", "bilder/schmetterling.bmp",
            "bilder/sonne.bmp", "bilder/wolke.bmp",
            "bilder/maus4.bmp"]

        self.karten = []
        
        # laedt die Karten in die Liste Karten
        bild_zaehler = 0
        schleife = 0
        while schleife < 42:
            self.karten.append(memorykarten.Memorykarte(
                self.bild_namen[bild_zaehler], bild_zaehler))
            if (schleife + 1) % 2 == 0:
                bild_zaehler += 1
            schleife += 1
        
        random.shuffle(self.karten)            
        self.spielfeld.setIconSize(QSize(64, 64))
           
        # laedt die Karten in der liste in die Tabelle
        for zeile in zeilen:
            for spalte in spalten:
                self.spielfeld.setItem(zeile, spalte, self.karten[(spalte * 7) + zeile])
                self.karten[(spalte * 7) + zeile].set_bild_pos((spalte * 7) + zeile)    
        
        self.show()
    
    def maus_klick_slot(self, x, y):
        if self.zug_erlaubt() == True:
            if (self.karten[(y * 7) + x].get_umgedreht() == False) and (self.karten[(y * 7) + x].get_noch_im_spiel() == True):
                self.karten[(y * 7) + x].umdrehen()
                self.karte_oeffnen(self.karten[(y * 7) + x])
            
    def timer_slot(self):
        self.karte_schliessen()
    
    def karte_oeffnen(self, karte):
        self.paar[self.umgedrehte_karten] = karte
        karten_id = karte.get_bild_ID()
        karten_pos = karte.get_bild_pos()
        
        if self.gemerkte_karten[0][karten_id] == -1:
            self.gemerkte_karten[0][karten_id] = karten_pos
        else:
            if self.gemerkte_karten[0][karten_id] != karten_pos:
                self.gemerkte_karten[1][karten_id] = karten_pos
                
        self.umgedrehte_karten += 1
        
        if self.umgedrehte_karten == 2:
            self.paar_pruefen(karten_id)
            self.timer_umdrehen.start(2000)
            
        if self.mensch_punkte + self.computer_punkte == 21:
            
            gewinner = self.label_text_mensch.text() if self.mensch_punkte > self.computer_punkte else self.label_text_computer.text()
            punkte = self.mensch_punkte if self.mensch_punkte > self.computer_punkte else self.computer_punkte
            
            self.timer_umdrehen.stop()
            QMessageBox.information(self, "Spielende", "Das Spiel ist vorbei."
                                    f"\nDer Gewinner ist der {gewinner}" 
                                    f"\nDer {gewinner} gewinnt mit {punkte} Punkten")  
            
            self.close()
        
    def paar_pruefen(self, karten_id):
        if self.paar[0].get_bild_ID() == self.paar[1].get_bild_ID():
            self.paar_gefunden()
            self.gemerkte_karten[0][karten_id] = -2
            self.gemerkte_karten[1][karten_id] = -2
            
    def paar_gefunden(self):
        if self.spieler == 0:
            self.mensch_punkte += 1
            self.label_mensch.setNum(self.mensch_punkte)
        else:
            self.computer_punkte += 1
            self.label_computer.setNum(self.computer_punkte)
            
    def karte_schliessen(self):
        raus = False
        
        if self.paar[0].get_bild_ID() == self.paar[1].get_bild_ID():
            self.paar[0].rausnehmen()
            self.paar[1].rausnehmen()
            raus = True
        else:
            self.paar[0].umdrehen()
            self.paar[1].umdrehen()
        
        self.umgedrehte_karten = 0
        
        if raus == False:
            self.spieler_wechseln()
        else:
            if self.spieler == 1:
                self.computer_zug()
    
    def spieler_wechseln(self):
        if self.vs_computer.isChecked():
            self.label_text_mensch.setText("Mensch")
            self.label_text_computer.setText("Computer")
            
            if self.spieler == 0:
                self.spieler = 1
                self.computer_zug()
                self.label_aktueller_spieler_anzeigen.setText("Computer")
            else:
                self.spieler = 0
                self.label_aktueller_spieler_anzeigen.setText("Mensch")

        elif self.vs_mensch.isChecked():
            self.label_text_mensch.setText("Spieler 1")
            self.label_text_computer.setText("Spieler 2")
            
            if self.spieler == 0:
                self.spieler = 2               
                self.label_aktueller_spieler_anzeigen.setText("Spieler 2")
                
            else:
                self.spieler = 0
                self.label_aktueller_spieler_anzeigen.setText("Spieler 1")

    def computer_zug(self):
        karten_zaehler = 0
        treffer = False
        
        if random.randint(0, self.spielstaerke) % self.spielstaerke == 0:
            while (karten_zaehler < 21) and (treffer == False):
                if (self.gemerkte_karten[0][karten_zaehler] >= 0) and (self.gemerkte_karten[1][karten_zaehler] >= 0):
                    treffer = True
                    self.karten[self.gemerkte_karten[0][karten_zaehler]].umdrehen()
                    self.karte_oeffnen(self.karten[self.gemerkte_karten[0][karten_zaehler]])
                    self.karten[self.gemerkte_karten[1][karten_zaehler]].umdrehen()
                    self.karte_oeffnen(self.karten[self.gemerkte_karten[1][karten_zaehler]])
            
                karten_zaehler += 1
            
        if (treffer == False):
            while True:
                zufall = random.randint(0, 41)
                if self.karten[zufall].get_noch_im_spiel() == True:
                    self.karten[zufall].umdrehen()
                    self.karte_oeffnen(self.karten[zufall])
                    break
                
            while True:
                zufall = random.randint(0, 41)
                if (self.karten[zufall].get_noch_im_spiel() == True) or (self.karten[zufall].get_umgedreht() == False):
                    self.karten[zufall].umdrehen()
                    self.karte_oeffnen(self.karten[zufall])
                    break
                
    def set_spielstaerke(self, staerke):
        self.spielstaerke = staerke
            
    def zug_erlaubt(self):
        erlaubt = True
        if (self.spieler == 1) or (self.umgedrehte_karten == 2):
            erlaubt = False
        return erlaubt

    def schummeln(self):
        if self.zug_erlaubt():
            self.schummeln_karten = []  
            for karte in self.karten:
                if karte.get_noch_im_spiel() and not karte.get_umgedreht():
                    karte.umdrehen()
                    self.schummeln_karten.append(karte) 
        self.schummeln_timer.start(2000)

    def schummeln_vorbei(self):
        for karte in self.schummeln_karten:
            karte.umdrehen()
        self.schummeln_karten = []
                   
