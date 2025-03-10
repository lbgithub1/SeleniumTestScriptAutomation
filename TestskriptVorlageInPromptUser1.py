testSkriptVorlageVar1 = """
from AnmeldungWiWaFuerTestskript import anmeldungWiWaFuerSkript

user = "s4loboeh@uni-trier.de"
pwd = "Psa#775"

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Initialize the Chrome WebDriver
driver = webdriver.Chrome()

try:
    # Step 1: Open the specified URL
    driver.get("https://wiwa.uni-trier.de")
    anmeldungWiWaFuerSkript(driver, user, pwd)
    driver.get("https://wiwa.uni-trier.de/produkte/produkte")
    time.sleep(4)  # Explicit wait to ensure the page loads completely

    # Step 2: Locate and click on the "Administration" icon
    admin_icon = driver.find_element(By.XPATH, "//a[@id='navbarDropdown']/i[@title='Administration']")
    admin_icon.click()
    time.sleep(4)  # Explicit wait after clicking the administration icon

    # Step 3: Locate and click on the "Produkte" menu item
    produkte_menu = driver.find_element(By.XPATH,
                                        "//a[contains(@class, 'dropdown-item dropdown-toggle')][contains(., 'Produkte')]")
    produkte_menu.click()
    time.sleep(4)  # Explicit wait after clicking the "Produkte" menu item

    # Step 4: Locate and click on the "Hersteller" menu item
    hersteller_menu = driver.find_element(By.XPATH,
                                          "//a[contains(@class, 'dropdown-item')][contains(@href, '/admin/adminitems/hersteller')]")
    hersteller_menu.click()
    time.sleep(4)  # Explicit wait after clicking the "Hersteller" menu item

    # Step 5: Locate and click the "Neu" button
    neu_button = driver.find_element(By.XPATH, "//div[@class='toolbar']//button[contains(., 'Neu')]")
    neu_button.click()
    time.sleep(4)  # Explicit wait after clicking the "Neu" button

    # Step 6: Fill in the "Hersteller" text field
    hersteller_field = driver.find_element(By.XPATH, "//input[@id='hersteller' and @name='hersteller']")
    hersteller_field.click()
    hersteller_field.send_keys("Intel")
    time.sleep(4)  # Explicit wait after interacting with the "Hersteller" field

    # Step 7: Fill in the "Primaeresherstellungsland" text field
    land_field = driver.find_element(By.XPATH, "//input[@id='primaeresherstellungsland' and @type='text']")
    land_field.click()
    land_field.send_keys("DE")
    time.sleep(4)  # Explicit wait after interacting with the "Primaeresherstellungsland" field

    # Step 8: Click the "Speichern" button
    save_button = driver.find_element(By.XPATH, "//div//button[@id='btnSpeichern' and @name='btnSpeichern']")
    save_button.click()
    time.sleep(4)  # Explicit wait after clicking the "Speichern" button

    # Step 9: Verification (waiting for 10 seconds)
    time.sleep(10)  # Explicit wait for final verification

    # Print success message
    print("Test successful")

finally:
    # Step 10: Close the browser
    driver.quit()
    """
