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
    Collects complaints titles and upvotes from Reclame Aqui and saves them to Excel.

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
    chrome_options.add_argument("--log-level=3")  # Suppress logs

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

    # Wait for complaints to load
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//h4[@data-testid='compain-title-link']"))
        )
    except TimeoutException:
        print("No complaints found.")
        driver.quit()
        return

    # Scroll to load more complaints if necessary
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # -----------------------------
    # Collect complaints data
    # -----------------------------
    titles = driver.find_elements(By.XPATH, "//h4[@data-testid='compain-title-link']")
    complaints_data = []

    for title in titles:
        complaint_text = title.text
        try:
            # Adjust XPath for upvotes if needed
            upvotes = title.find_element(By.XPATH, ".//following::span[contains(@class,'upvotes')]").text
        except:
            upvotes = None
        complaints_data.append({
            "complaint_title": complaint_text,
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
