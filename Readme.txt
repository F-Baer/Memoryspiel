Dieses Projekt ist eine Implementierung eines klassischen Memory-Spiels in Python, das mit **PyQt5** erstellt wurde. Die Anwendung enthält eine grafische Benutzeroberfläche (GUI), in der zwei Spieler gegeneinander antreten können, oder es kann gegen den Computer gespielt werden.

Hauptkomponenten
- **memoryspiel.py**: Diese Datei enthält die Spiellogik des Memory-Spiels. Hier wird das Spiel gestartet, die Karten aufgedeckt und überprüft, ob zwei Karten übereinstimmen.
- **memorykarten.py**: Diese Datei enthält die Klasse `Memorykarte`, die für die Darstellung und Verwaltung der einzelnen Karten verantwortlich ist. Jede Karte hat ein 				zugeordnetes Bild und einen Status, der festlegt, ob die Karte aufgedeckt oder verdeckt ist.
- **bilder/**: Dieser Ordner enthält die Bilddateien der Memory-Karten, die im Spiel verwendet werden. Die Bilder müssen korrekt benannt sein und im PNG-Format vorliegen.

Projekt-Setup
- Stelle sicher, dass die memoryspiel.py und memorykarten.py unter dem Verzeichnis Spieldaten gespeichert sind. 
- Stelle sicher das die Bild Dateien im Ordner Bilder untergebracht sind und dieser Ordner in dem selben Ordner wie das Hauptprogramm.
- Starte das Programm mit Memoryspiel_Start.py

Nutzung
Das Spiel startet mit einem Auswahlmenü, in dem der Spieler wählen kann, ob er gegen einen menschlichen Mitspieler oder gegen den Computer spielen möchte. Im Spiel selbst wird durch Klicken auf eine verdeckte Karte diese aufgedeckt. Das Ziel ist es, Paare von Karten zu finden, die identische Bilder zeigen.

Modul memorykarten
Die Memorykarte Klasse erbt von QTableWidgetItem aus PyQt5 und repräsentiert eine einzelne Karte im Memory-Spiel. Sie verwaltet das visuelle Erscheinungsbild der Karte und deren Status (verdeckt, aufgedeckt oder aus dem Spiel entfernt).

Hauptattribute:
- bild_vorne: Speichert das vordere Bild der Karte (Icon), welches dargestellt wird, wenn die Karte aufgedeckt wird.
- bild_hinten: Enthält das Standardbild für die Rückseite der Karte (Icon), welches angezeigt wird, solange die Karte verdeckt ist.
- umgedreht: Ein boolescher Wert, der den Status der Karte bestimmt. Ist er True, ist die Karte aufgedeckt, sonst ist sie verdeckt.
- noch_im_spiel: Bestimmt, ob die Karte noch im Spiel ist (True) oder bereits aus dem Spiel entfernt wurde (False).
- bild_ID: Eine eindeutige ID zur Identifikation des Bildes, das auf der Vorderseite der Karte angezeigt wird.
- bild_pos: Speichert die Position der Karte im Raster des Spielfelds.

Methoden:
- umdrehen(): Diese Methode dreht die Karte um. Wenn die Karte verdeckt ist, wird das Vorderbild (bild_vorne) angezeigt, andernfalls wird die Rückseite (bild_hinten) 		      dargestellt.
- rausnehmen(): Entfernt die Karte aus dem Spiel, indem ein spezielles Bild angezeigt wird, welches angibt, dass die Karte nicht mehr aufgedeckt werden kann.
- get_bild_ID(): Gibt die ID des Bildes zurück, das mit der Karte verbunden ist. Diese ID wird zur Überprüfung von Kartenpaaren verwendet.
- get_bild_pos() und set_bild_pos(position): Diese Methoden werden verwendet, um die Position der Karte auf dem Spielfeld zu setzen bzw. abzurufen.
- get_noch_im_spiel(): Liefert zurück, ob die Karte noch im Spiel ist.
- get_umgedreht(): Liefert den Status zurück, ob die Karte umgedreht ist (aufgedeckt).

Modul memoryspiel
Die Memoryspiel-Klasse erbt von QWidget und implementiert die gesamte Logik und das grafische Interface des Memory-Spiels. Sie steuert das Spielfeld, die Spielabläufe, die Spieler-Interaktionen sowie die Spielmodus-Auswahl (Spiel gegen einen anderen Menschen oder gegen den Computer).

Hauptattribute:
- spielfeld: Ein 7x6 QTableWidget, das als Spielfeld für die Memory-Karten dient.
- spieler: Ein Integer-Wert, der den aktuellen Spieler angibt. 0 steht für den menschlichen Spieler, 1 für den Computer.
- mensch_punkte und computer_punkte: Zähler für die Punkte der Spieler.
- umgedrehte_karten: Zählt die Anzahl der aktuell aufgedeckten Karten (maximal 2).
- gemerkte_karten: Eine Liste, die die Positionen der Karten speichert, die der Computer "gesehen" hat, um sie später wiederzufinden.
- spielstaerke: Stellt den Schwierigkeitsgrad für den Computergegner ein. Ein niedrigerer Wert bedeutet, dass der Computer bessere Züge macht.

Spielfeld und Layout:
Das Spielfeld besteht aus einer 7x6 Tabelle, in die Karten geladen werden. Jede Karte repräsentiert ein QTableWidgetItem, das aufgedeckt oder verdeckt werden kann. Neben dem Spielfeld gibt es mehrere Labels, die den aktuellen Spieler, die Punktzahl und den Spielmodus anzeigen. Ein Schummeln-Button ermöglicht es dem Spieler, für einen kurzen Zeitraum alle verdeckten Karten aufzudecken.

Spielmodi:
Die Klasse unterstützt zwei Spielmodi:

1. Mensch gegen Computer: Hierbei spielt der menschliche Spieler gegen den Computer.
2. Mensch gegen Mensch: Zwei menschliche Spieler treten gegeneinander an.

Über die Radio-Buttons kann der gewünschte Spielmodus und die Spielstärke für den Computer ausgewählt werden.

Methoden:
- maus_klick_slot(x, y): Wird aufgerufen, wenn der Spieler auf eine Karte klickt. Diese Methode dreht die Karte um, wenn der Zug erlaubt ist.
- karte_oeffnen(karte): Fügt die aufgedeckte Karte zum aktuellen Paar hinzu und prüft, ob zwei Karten aufgedeckt wurden.
- paar_pruefen(karten_id): Prüft, ob das aktuell aufgedeckte Kartenpaar übereinstimmt. Wenn ja, werden die Karten entfernt.
- karte_schliessen(): Dreht die Karten wieder um, wenn sie nicht übereinstimmen.
- spieler_wechseln(): Wechselt den Spieler, nachdem ein Zug abgeschlossen wurde.
- computer_zug(): Führt den Zug des Computers durch. Der Computer merkt sich Karten, die er zuvor aufgedeckt hat, um strategisch vorzugehen, basierend auf der eingestellten 
		Spielstärke.
- schummeln(): Der menschliche Spieler kann über diese Funktion für kurze Zeit alle verdeckten Karten aufdecken. Nach 2 Sekunden werden die Karten wieder verdeckt.

Spielende:
Das Spiel endet, wenn alle 21 Kartenpaare gefunden wurden. Der Spieler mit den meisten Punkten gewinnt, und das Ergebnis wird in einem QMessageBox-Dialogfenster angezeigt.

Computer-Spielstärke:
Es gibt vier Schwierigkeitsstufen:

- Leicht: Der Computer merkt sich weniger Karten und spielt dadurch weniger effizient.
- Mittel: Der Computer spielt ausgewogen, indem er einige Karten im Gedächtnis behält.
- Schwer: Der Computer merkt sich viele Karten und spielt sehr effizient.
- Extrem: Der Computer kann sich nahezu alle Karten merken und spielt nahezu perfekt.

Verwendung:
Die Klasse Memorykarte wird für jede Karte im Memory-Spiel instanziiert. Jede Karte startet verdeckt mit der Rückseite (bild_hinten). Wenn der Spieler auf eine Karte klickt, wird die Methode umdrehen() aufgerufen, um sie aufzudecken oder wieder zu verdecken. Sobald ein Kartenpaar gefunden wird, wird die Methode rausnehmen() verwendet, um die Karten aus dem Spiel zu entfernen.

Wichtige Hinweise
Die Bilddateien müssen sich im Ordner bilder/ befinden und korrekt benannt sein, damit sie im Spiel korrekt angezeigt werden.
Sollten Kartenbilder nicht geladen werden, stelle sicher, dass der Pfad zu den Bilddateien in der memorykarten.py korrekt gesetzt ist.

Weiterentwicklung
Füge neue Features hinzu wie z. B. zusätzliche Schwierigkeitsstufen oder neue Kartensets.
Verbessere die Benutzeroberfläche oder integriere weitere Spielmodi.