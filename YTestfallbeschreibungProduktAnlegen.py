testfallbeschreibungVar = """
Ziel des Testfalls:
Überprüfen, ob das Anlegen neuer Produkte im WiWa-Systems (URL="https://wiwa.uni-trier.de") funktioniert. 
Der Test soll sicherstellen, dass ein Benutzer ein neues Produkt anlegen kann. 
 
Umgebung und Voraussetzungen:
- Das Testskript soll in Python geschrieben sein.
- Es soll die Selenium-Bibliothek verwenden.
- Als Browser soll Chrome (mit entsprechendem ChromeDriver) verwendet werden.
- Alle notwendigen Importe (z. B. from selenium import webdriver, from selenium.webdriver.common.by import By, from selenium.webdriver.support.ui import WebDriverWait, from selenium.webdriver.support import expected_conditions as EC) sollen automatisch integriert werden.
- Explizite Wait-Mechanismen nutzen, um auf das Laden von Seiten oder Elementen zu warten (mind. einen expliziten Wait mit WebDriverWait).
- Der Code soll gut auskommentiert sein, um auch weniger erfahrenen Personen das Verständnis über den Code zu erleichtern.
- Achte bei der Erstellung der Selektoren auf einzigartige Attirbute wie id oder class im HTML-Code

Testschritte:
1. Browser starten:
- Öffne eine Chrome-Browser-Instanz über den ChromeDriver.

2. Seite aufrufen:
- Navigiere zur URL: "https://wiwa.uni-trier.de/produkte/produkt/0/0/0".
- Warte 4 Sekunden explizit darauf, dass die Startseite vollständig geladen ist.

3. Hersteller auswählen:
- Positionierung: Das Hersteller-Selektionsmenü befindet sich oben links und hat den name="herstellerid".
- Beschreibung: Es handelt sich um ein Seleketionsmenü, welche den Namen und die ID="herstellerid" besitzt.
- Klicke auf das selections Menü.
- Warte explizit 4 Sekunden.

4. Option auswählen:
- Positionierung: Sobald auf das Hersteller-Selektionsmenü geklickt wurde erscheinen mehrere Optionen.
- Beschreibung: Klicke auf die zweite Option="DHL".
- Warte explizit 4 Sekunden.

5. Klicke auf  Speichern & schließen:
- Nachdem du den Hersteller geändert hast, klicke auf den Speichern & schließen Button.
- Der Button besitzt den type="button", den name="btnSpeichernSchliessen", die id="btnSpeichernSchliessen" und befindet sich in einem div-Tag.
- Warte explizit 4 Sekunden.


6. Überprüfung des Tests: 
- Wenn du den Button gedrückt hast, muss die URL wie folgt lauten: "https://wiwa.uni-trier.de/reports/reports"


7. Test beenden:
- Schließe den Browser.
"""