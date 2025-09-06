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

def collect_reclameaqui_data(company_name, excel_path, chromedriver_path):
    """
    Collects company data from Reclame Aqui and saves it to an Excel file.

    Args:
        company_name (str): The company's name in the Reclame Aqui URL.
        excel_path (str): Path to the Excel file to save the data.
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
    # Access company page
    # -----------------------------
    url = f"https://www.reclameaqui.com.br/empresa/{company_name}/"
    driver.get(url)

    # Accept cookies if popup appears
    try:
        cookie_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[2]/a[1]'))
        )
        cookie_button.click()
    except TimeoutException:
        print("No cookies pop-up found.")

    # Scroll a bit to make sure elements are visible
    driver.execute_script("window.scrollBy(0, 300)")

    # -----------------------------
    # Define elements to scrape
    # -----------------------------
    elements = {
        'overall_rating': '//*[@id="reputation"]/div[1]/div[1]/div[2]/span[2]/b',
        'num_complaints': '//*[@id="reputation"]/div[1]/div[2]/a[1]/div/div/b',
        'num_answered': '//*[@id="reputation"]/div[1]/div[2]/a[2]/div/div/b',
        'percent_answered': '//*[@id="reputation"]/div[2]/div[1]/div[1]/span',
        'new_negotiations': '//*[@id="reputation"]/div[2]/div[1]/div[2]/span',
        'solution_index': '//*[@id="reputation"]/div[2]/div[1]/div[3]/span',
        'consumer_rating': '//*[@id="reputation"]/div[2]/div[1]/div[4]/span'
    }

    # -----------------------------
    # Collect data
    # -----------------------------
    data = {}
    for key, xpath in elements.items():
        try:
            element = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, xpath))
            )
            data[key] = element.text.strip()
        except TimeoutException:
            data[key] = None
            print(f"Element {key} not found.")

    # Add timestamp
    now = datetime.datetime.now()
    data['date'] = now.date()
    data['time'] = now.time()

    driver.quit()

    # -----------------------------
    # Save to Excel
    # -----------------------------
    if os.path.exists(excel_path):
        existing_df = pd.read_excel(excel_path)
        new_row = pd.DataFrame([data])
        df = pd.concat([existing_df, new_row], ignore_index=True)
    else:
        df = pd.DataFrame([data])

    df.to_excel(excel_path, index=False)
    print(f"Data saved to {excel_path}")


# -----------------------------
# Example usage
# -----------------------------
chromedriver_path = "C:/Users/Lior Lerner/Downloads/chromedriver-win64/chromedriver.exe"
excel_path = "reclameaqui_santander.xlsx"
collect_reclameaqui_data("santander", excel_path, chromedriver_path)
