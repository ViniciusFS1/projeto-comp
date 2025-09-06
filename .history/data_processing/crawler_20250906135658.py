# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Define path to chromedriver
chromedriver_path = 'c:\\Users\\Lior Lerner\\Downloads\\chromedriver-win64\\chromedriver.exe'

# Set Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # Open browser maximized
chrome_options.add_argument("--disable-notifications")  # Disable pop-ups
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-extensions")

# Initialize Chrome driver with Service and options
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Define the company name and URL
company_name = 'Santander'  # Replace with the target company
url = f"https://www.reclameaqui.com.br/empresa/{company_name}/"
driver.get(url)

# Wait for cookies pop-up and click "accept" if present
try:
    cookie_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[2]/a[1]'))
    )
    cookie_button.click()
except:
    print("No cookies pop-up found.")

# Scroll a bit to make sure elements are visible
driver.execute_script("window.scrollBy(0, 300)")
