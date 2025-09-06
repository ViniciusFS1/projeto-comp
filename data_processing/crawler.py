from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pandas as pd
import datetime
import os
import time

def collect_complaints(company_name: str, csv_path: str, chromedriver_path: str, pages: int = 1) -> None:
    """
    Collects complaints (title, text, upvotes) from Reclame Aqui and saves them to CSV.

    Args:
        company_name (str): Company name in the Reclame Aqui URL.
        csv_path (str): Path to the CSV file to save data.
        chromedriver_path (str): Path to chromedriver.exe.
        pages (int): Number of pages to collect (default=1).
    """
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--log-level=3")  
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    url = f"https://www.reclameaqui.com.br/empresa/{company_name}/lista-reclamacoes/"
    driver.get(url)

    try:
        cookie_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[2]/a[1]'))
        )
        cookie_button.click()
    except TimeoutException:
        print("No cookies pop-up found.")

    complaints_data = []

    for page_num in range(pages):
        print(f"Collecting page {page_num + 1}...")

        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//h4[@data-testid='compain-title-link']"))
            )
        except TimeoutException:
            print("No complaints found on this page.")
            break

        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        titles = driver.find_elements(By.XPATH, "//h4[@data-testid='compain-title-link']")

        for title in titles:
            complaint_title = title.text

            try:
                complaint_text = title.find_element(
                    By.XPATH, ".//following::p[contains(@class,'sc-1pe7b5t-2')]"
                ).text
            except:
                complaint_text = None

            try:
                upvotes = title.find_element(
                    By.XPATH, ".//following::span[contains(@class,'upvotes')]"
                ).text
            except:
                upvotes = None

            complaints_data.append({
                "complaint_title": complaint_title,
                "complaint_text": complaint_text,
                "upvotes": upvotes,
                "date_collected": datetime.datetime.now().date(),
                "time_collected": datetime.datetime.now().time()
            })

        try:
            next_button = driver.find_element(By.XPATH, "//button[@data-testid='next-page-navigation-button']")
            driver.execute_script("arguments[0].click();", next_button)
            time.sleep(2)
        except NoSuchElementException:
            print("No more pages found.")
            break

    driver.quit()

    # Save to CSV
    df_new = pd.DataFrame(complaints_data)

    if os.path.exists(csv_path):
        df_existing = pd.read_csv(csv_path)
        df = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df = df_new

    df.to_csv(csv_path, index=False)
    print(f"{len(df_new)} complaints saved to {csv_path}")

