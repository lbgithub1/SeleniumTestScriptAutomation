from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from dotenv import load_dotenv
import os
from bs4 import Comment
import tiktoken

user = "s4loboeh@uni-trier.de"
pwd = "Psa#775"
def anmeldungWiWa(url):


    # WebDriver-Setup
    driver = webdriver.Chrome()  # Verwende den Pfad zu deinem WebDriver, falls notwendig
    driver.maximize_window()

    # Öffne die URL
    driver.get("https://wiwa.uni-trier.de/produkte/produkte")
    time.sleep(3)  # Warte, bis die Seite vollständig geladen ist

    # Suche den Button oder Link mit dem Text "Mietobjekte ansehen!" und klicke darauf
    try:
        userBox = driver.find_element(By.XPATH, '//*[@id="email"]')
        userBox.click()
        for x in user:
            time.sleep(0.05)
            userBox.send_keys(x)

        time.sleep(4)  # Warte, bis die Mietobjekte-Seite vollständig geladen ist

        pwdBox = userBox = driver.find_element(By.XPATH, '//*[@id="password"]')
        pwdBox.click()
        for y in pwd:
            time.sleep(0.05)
            pwdBox.send_keys(y)

        time.sleep(2)
        logInButton = driver.find_element(By.XPATH, '//*[@id="btnsubmit"]')
        logInButton.click()
        time.sleep(3)
        #Welche Seite letzendlich dann untersucht werden soll, deswegen hier erneuter Aufruf, erster Aufruf nicht genug
        driver.get(url)
        time.sleep(3)
        html = driver.page_source

        print("Test erfolgreich durchgeführt.")
        time.sleep(2)
        return html
    except Exception as e:
        print(f"Fehler beim Test: {e}")


def htmlCodeHelper(url):
    driver = webdriver.Chrome()  # Verwende den Pfad zu deinem WebDriver, falls notwendig
    driver.maximize_window()
    driver.get(url)
    time.sleep(10)
    html = driver.page_source
    return html






if __name__ == "__main__":
    datei2 = "CleanedWaWi.html"
    url = "https://wiwa.uni-trier.de/produkte/produkte"

