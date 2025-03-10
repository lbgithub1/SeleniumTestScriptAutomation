testfallbeschreibungVar = """
Ziel des Testfalls:
Überprüfen, ob die Anmeldung im WiWa-System (URL="https://wiwa.uni-trier.de/") erfolgreich durchgeführt werden kann.
Der Test soll sicherstellen, dass ein Benutzer mit den Zugangsdaten korrekt authentifiziert wird und auf die Startseite des Systems weitergeleitet wird.
eMail /username="s4loboeh@uni-trier.de"
Passwort="Psa#775"
Es handelt sich um einen statischen Login-Prozess, bei dem Benutzername und Passwort eingegeben und auf die Schaltfläche „Anmelden“ geklickt werden.

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
- Navigiere zur URL="https://wiwa.uni-trier.de/".
- Warte 4 Sekunden explizit darauf, dass die Startseite vollständig geladen ist.

3. Benutzername eingeben:
- Positionierung: Das Eingabefeld für den Benutzernamen befindet sich im oberen Bereich des Formulars.
- Beschreibung: Es handelt sich um ein Text input-Element mit der id="email" und der class="form-control".
- Füge den Benutzernamen="s4loboeh@uni-trier.de" in das Eingabefeld ein.
- Warte explizit 4 Sekunden.

4. Passwort eingeben:
- Positionierung: Das Eingabefeld für das Passwort befindet sich unterhalb des Benutzernamenfelds im Formular.
- Beschreibung: Es handelt sich um ein input-Element mit id="password" und der class="form-control".
- Füge das Passwort="Psa#775" in das Eingabefeld ein.
- Warte explizit 4 Sekunden.

5. Einloggen:
- Positionierung: Die Schaltfläche "Einloggen" befindet sich unterhalb des Eingabefelds Passwort.
- Beschreibung: Es handelt sich um ein button-Tag, mit der id="btnsubmit" und der class="btn btn-secondary".
- Klicke auf die Schaltfläche "Einloggen".
- Warte explizit 4 Sekunden.

6. Überprüfung des Tests: 
- Wenn du auf das Produkt geklickt hast, muss die URL wie folgt lauten="https://wiwa.uni-trier.de/home/dashboard/1/0"

7. Test beenden:
- Schließe den Browser.
"""