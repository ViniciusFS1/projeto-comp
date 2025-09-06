from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import datetime
import os
import time

def collect_complaints(company_name, excel_path, chromedriver_path):
    """
    Collects complaints and upvotes from Reclame Aqui and saves them to Excel.

    Args:
        company_name (str): Company name in the Reclame Aqui URL.
        excel_path (str): Path to the Excel file to save data.
        chromedriver_path (str): Path to chromedriver.exe.
    """
    # -----------------------------
    # Chrome setup
    # -----------------------------
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")

    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # -----------------------------
    # Access complaints page
    # -----------------------------
    url = f"https://www.reclameaqui.com.br/empresa/{company_name}/lista-reclamacoes/"
    driver.get(url)

    # Accept cookies if popup appears
    try:
        cookie_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[2]/a[1]'))
        )
        cookie_button.click()
    except TimeoutException:
        print("No cookies pop-up found.")

    # Wait for complaints container to load
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class,"sc-1b5q6xg-1")]'))
        )
    except TimeoutException:
        print("No complaints found.")
        driver.quit()
        return

    # -----------------------------
    # Scroll down to load more complaints (if necessary)
    # -----------------------------
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # -----------------------------
    # Collect complaints
    # -----------------------------
    complaints_elements = driver.find_elements(By.XPATH, '//div[contains(@class,"sc-1b5q6xg-1")]')
    complaints_data = []

    for elem in complaints_elements:
        try:
            text = elem.find_element(By.XPATH, './/p').text
        except:
            text = None
        try:
            upvotes = elem.find_element(By.XPATH, './/span[contains(@class,"upvotes")]').text
        except:
            upvotes = None

        complaints_data.append({
            "complaint_text": text,
            "upvotes": upvotes,
            "date_collected": datetime.datetime.now().date(),
            "time_collected": datetime.datetime.now().time()
        })

    driver.quit()

    # -----------------------------
    # Save to Excel
    # -----------------------------
    df_new = pd.DataFrame(complaints_data)

    if os.path.exists(excel_path):
        df_existing = pd.read_excel(excel_path)
        df = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df = df_new

    df.to_excel(excel_path, index=False)
    print(f"{len(df_new)} complaints saved to {excel_path}")


