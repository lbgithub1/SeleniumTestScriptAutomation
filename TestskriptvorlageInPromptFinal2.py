testSkriptVorlageVar2 = """
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
user = "s4loboeh@uni-trier.de"
pwd = "Psa#775"

# Initialize the Chrome WebDriver
driver = webdriver.Chrome()

try:
    # Step 1: Open the specified URL
    driver.get("https://wiwa.uni-trier.de/produkte/produkte")
    anmeldungWiWaFuerSkript(driver, user, pwd)
    driver.get("https://wiwa.uni-trier.de/produkte/produkte")
    time.sleep(4)  # Explicit wait to ensure the page loads completely

    # Step 2: Locate and click on the search bar
    search_bar = driver.find_element(By.XPATH, "//input[@type='search' and @placeholder='Suchen']")
    search_bar.click()
    time.sleep(4)  # Explicit wait after clicking the search bar

    # Step 3: Enter the product name in the search bar
    search_bar.send_keys("Canon Pixma TS7450i")
    time.sleep(4)  # Explicit wait after entering product name

    # Step 4: Select the product from the table after search
    product_link = driver.find_element(By.XPATH, "//td/a[contains(text(), 'Canon Pixma TS7450i')]")
    product_link.click()
    time.sleep(4)  # Explicit wait after clicking the product link

    # Step 5: Locate the "Notizen" text field on product properties page
    notes_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//textarea[@id='notizen' and @name='notizen' and @placeholder='Notizen...']"))
    )
    notes_field.click()
    time.sleep(4)
    notes_field.clear()
    notes_field.send_keys("3-in-1-Multifunktionssystem im zweifarbigen Design mit LED-Statusleiste")
    time.sleep(4)

    # Step 6: Click on the "Speichern & schließen" button to save the note
    save_button = driver.find_element(By.XPATH, "//button[@id='btnSpeichernSchliessen' and @name='btnSpeichernSchliessen' and @type='button']")
    save_button.click()
    time.sleep(4)  # Explicit wait after clicking the "Save & Close" button

    # Step 7: Verify the URL after saving changes
    assert driver.current_url == "https://wiwa.uni-trier.de/produkte/produkte", "URL verification failed!"

    # Print success message
    print("Test successful")


finally:
    # Step 8: Close the browser
    driver.quit()
"""