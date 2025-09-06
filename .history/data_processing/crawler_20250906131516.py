from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def crawl_reclameaqui(email: str, password: str, company: str, wait_time: int = 5, scroll_pause: int = 2, output_file: str = None) -> list:
    """
    Crawl ReclameAqui complaints for a specific company after logging in.
    
    Args:
        email: Your ReclameAqui login email.
        password: Your password.
        company: Company slug in the URL (e.g., 'santander').
        wait_time: Seconds to wait for elements to load.
        scroll_pause: Seconds to pause while scrolling to load more complaints.
        output_file: Optional CSV file path to save complaints.
        
    Returns:
        List of complaint strings.
    """
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Uncomment to run headless
    options.add_argument("--disable-gpu")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # Login
        driver.get("https://www.reclameaqui.com.br/login")
        WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.NAME, "email"))
        ).send_keys(email)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # Wait until login completes
        WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "header"))
        )

        # Navigate to complaints
        driver.get(f"https://www.reclameaqui.com.br/empresa/{company}/reclamacoes/")
        WebDriverWait(driver, wait_time).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.sc-1pe7b5t-0"))
        )

        # Scroll to load more
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

        # Save to CSV if file provided
        if output_file:
            import csv
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
    EMAIL = "your_email@example.com"
    PASSWORD = "your_password"
    COMPANY = "santander"

    complaints = crawl_reclameaqui(EMAIL, PASSWORD, COMPANY, output_file=f"{COMPANY}_complaints.csv")
    print(f"Total complaints captured: {len(complaints)}")
    for idx, c in enumerate(complaints, 1):
        print(f"{idx}. {c}\n")
