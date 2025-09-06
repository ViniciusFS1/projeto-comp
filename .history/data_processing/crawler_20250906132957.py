from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv
import os

def crawl_reclameaqui_logged_in(company: str, profile_path: str, wait_time: int = 5, scroll_pause: int = 2, output_file: str = None) -> list:
    """
    Crawl ReclameAqui complaints for a company assuming the user is already logged in.

    Args:
        company: Company slug in the URL (e.g., 'santander').
        profile_path: Path to the Chrome user profile where the user is logged in.
        wait_time: Seconds to wait for elements to load.
        scroll_pause: Seconds to pause while scrolling.
        output_file: Optional CSV file path to save complaints.

    Returns:
        List of complaint strings.
    """
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_path}")  # use existing Chrome profile
    options.add_argument("--disable-gpu")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # options.add_argument("--headless")  # optional, may cause issues with some sites

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # Navigate directly to the company complaints page
        driver.get(f"https://www.reclameaqui.com.br/empresa/{company}/reclamacoes/")
        WebDriverWait(driver, wait_time).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.sc-1pe7b5t-0"))
        )

        # Scroll to load all complaints
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Capture complaints
        complaint_elements = driver.find_elements(By.CSS_SELECTOR, "div.sc-1pe7b5t-0")
        complaints = [el.text.strip() for el in complaint_elements if el.text.strip()]

        # Save to CSV if requested
        if output_file:
            with open(output_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Complaint"])
                for c in complaints:
                    writer.writerow([c])

        return complaints

    finally:
        driver.quit()


# -----------------------------
# Example usage
# -----------------------------
if __name__ == "__main__":
    COMPANY = "santander"
    PROFILE_PATH = r"C:/Users/YourUser/AppData/Local/Google/Chrome/User Data"  # path to Chrome profile with login

    complaints = crawl_reclameaqui_logged_in(
        company=COMPANY,
        profile_path=PROFILE_PATH,
        output_file=f"{COMPANY}_complaints.csv"
    )

    print(f"Total complaints captured: {len(complaints)}")
    for idx, c in enumerate(complaints, 1):
        print(f"{idx}. {c}\n")
