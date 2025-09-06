from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

def crawl_reclameaqui(company: str, wait_time: int = 5, scroll_pause: int = 2, output_file: str = None, profile_path: str = None) -> list:
    """
    Crawl ReclameAqui complaints for a specific company, handling login automatically.

    Args:
        company: Company slug in the URL (e.g., 'santander').
        wait_time: Seconds to wait for elements to load.
        scroll_pause: Seconds to pause while scrolling.
        output_file: Optional CSV file path to save complaints.
        profile_path: Optional path to Chrome user profile (to reuse login session).

    Returns:
        List of complaint strings.
    """
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Uncomment to run headless
    options.add_argument("--disable-gpu")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    if profile_path:
        options.add_argument(f"user-data-dir={profile_path}")  # reuse existing Chrome profile

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # Step 1: Open the company complaints page
        driver.get(f"https://www.reclameaqui.com.br/empresa/{company}/reclamacoes/")

        # Step 2: Check if login is required
        time.sleep(3)  # short pause to load page
        page_text = driver.page_source.lower()
        if "login" in page_text or "senha" in page_text or "e-mail" in page_text:
            print("[INFO] Login required. Please log in manually in the browser window.")
            driver.get("https://www.reclameaqui.com.br/login")
            WebDriverWait(driver, 300).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "header"))  # waits until login completes
            )
            print("[INFO] Login detected. Continuing...")

            # Navigate to company page again
            driver.get(f"https://www.reclameaqui.com.br/empresa/{company}/reclamacoes/")

        # Step 3: Wait for complaints to load
        WebDriverWait(driver, wait_time).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.sc-1pe7b5t-0"))
        )

        # Step 4: Scroll to load more complaints
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Step 5: Capture complaints
        complaint_elements = driver.find_elements(By.CSS_SELECTOR, "div.sc-1pe7b5t-0")
        complaints = [el.text.strip() for el in complaint_elements if el.text.strip()]

        # Step 6: Save to CSV if needed
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
    PROFILE_PATH = "C:/Users/YourUser/AppData/Local/Google/Chrome/User Data"  # optional

    complaints = crawl_reclameaqui(
        company=COMPANY,
        output_file=f"{COMPANY}_complaints.csv",
        profile_path=PROFILE_PATH
    )

    print(f"Total complaints captured: {len(complaints)}")
    for idx, c in enumerate(complaints, 1):
        print(f"{idx}. {c}\n")
