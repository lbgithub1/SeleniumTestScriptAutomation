#Produktlinie, welche gelöscht werden kann, muss vorher erstellt werden
# URL der Produktlinie muss entsprechend angepasst werden

testfallbeschreibungVar = """
Ziel des Testfalls:
Überprüfen ob ein Produkt gelöscht und anschließend die Produktübersichtsseite aufgerufen werden kann.
Arbeite alle Testschritte sequentiell nacheinander ab.

Umgebung und Voraussetzungen:
- Das Testskript soll in Python geschrieben sein.
- Es soll die Selenium-Bibliothek verwenden.
- Als Browser soll Chrome (mit entsprechendem ChromeDriver) verwendet werden.
- Alle notwendigen Importe (z. B. from selenium import webdriver, from selenium.webdriver.common.by import By, from selenium.webdriver.support.ui import WebDriverWait, from selenium.webdriver.support import expected_conditions as EC) sollen automatisch integriert werden.
- Explizite Wait-Mechanismen nutzen, um auf das Laden von Seiten oder Elementen zu warten (mind. einen expliziten Wait mit WebDriverWait).
- Der Code soll auskommentiert sein, um Personen mit geringer Programmierexpertise das Verständnis für den Code zu erleichtern.
- Achte bei der Erstellung der Selektoren auf einzigartige Attribute wie "id" oder "class" im HTML-Code.
- Generiere deine Testskripte gemäßt der Testskriptvorlagen und integriere, die anmeldungWiWaFuerSkript()-Methode.
- Integriere ebenfalls den Import der Methode "from AnmeldungWiWaFuerTestskript import anmeldungWiWaFuerSkript".

Testschritte:
1. Browser starten:
- Öffne eine Chrome-Browser-Instanz über den ChromeDriver.
- Navigiere zur URL="https://wiwa.uni-trier.de/produkte/produktlinien".

2. Seite aufrufen:
- Navigiere zur URL="https://wiwa.uni-trier.de//produkte/produktlinie/16/1/0".
- Warte 4 Sekunden explizit darauf, dass die Startseite vollständig geladen ist.

3. Produkt löschen:
- Scrolle zum unteren Bildschirmrand.
- Suche nach dem Button zum Loeschen des Produkts, welcher sich in einem button-Tag mit dem type="button" und dem name="btnLoeschen". 
- Klicke auf den Button zum Loeschen des Produkts.
- Warte explizit 4 Sekunden.

4. Überprüfung des Tests: 
- Wenn auf den Button "loeschen" geklickt wurde, muss die URL wie folgt lauten="https://wiwa.uni-trier.de/produkte/produktlinien".
- Warte explizit 4 Sekunden.
"""