# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import datetime
import os

# -----------------------------
# Chrome setup
# -----------------------------
chromedriver_path = 'c:\\Users\\Lior Lerner\\Downloads\\chromedriver-win64\\chromedriver.exe'

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-extensions")

service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# -----------------------------
# Define company and URL
# -----------------------------
company_name = 'santander'  # Replace with target company
url = f"https://www.reclameaqui.com.br/empresa/{company_name}/"
driver.get(url)

# Accept cookies if popup appears
try:
    cookie_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[2]/a[1]'))
    )
    cookie_button.click()
except:
    print("No cookies pop-up found.")

driver.execute_script("window.scrollBy(0, 300)")

# -----------------------------
# Collect data
# -----------------------------
# Define XPaths of elements to scrape
elements = {
    'overall_rating': '//*[@id="reputation"]/div[1]/div[1]/div[2]/span[2]/b',
    'num_complaints': '//*[@id="reputation"]/div[1]/div[2]/a[1]/div/div/b',
    'num_answered': '//*[@id="reputation"]/div[1]/div[2]/a[2]/div/div/b',
    'percent_answered': '//*[@id="reputation"]/div[2]/div[1]/div[1]/span',
    'new_negotiations': '//*[@id="reputation"]/div[2]/div[1]/div[2]/span',
    'solution_index': '//*[@id="reputation"]/div[2]/div[1]/div[3]/span',
    'consumer_rating': '//*[@id="reputation"]/div[2]/div[1]/div[4]/span'
}

data = {}
for key, xpath in elements.items():
    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        data[key] = element.text
    except:
        data[key] = None  # If element not found

# Add timestamp
now = datetime.datetime.now()
data['date'] = now.date()
data['time'] = now.time()

driver.quit()

# -----------------------------
# Save to Excel
# -----------------------------
file_path = 'reclameaqui_data.xlsx'

# Check if file exists
if os.path.exists(file_path):
    df = pd.read_excel(file_path)
else:
    df = pd.DataFrame()  # create empty DataFrame if file does not exist

# Transform data dictionary into a DataFrame
new_row = pd.DataFrame([data])

# Concatenate the new row
df = pd.concat([df, new_row], ignore_index=True)

# Save to Excel
df.to_excel(file_path, index=False)
print(f"Data saved to {file_path}")