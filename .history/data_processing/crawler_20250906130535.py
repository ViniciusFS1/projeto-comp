from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re
import time
import os


def crawler(url: str, target: str, save_file_path: str, wait_time: int = 5, debug: bool = False) -> list:
    """
    Crawler using Selenium

    Args:
        url: Target website to be analyzed by the crawler (str)
        target: Desired word or sentence to be located (str)
        save_file_path: Path to the .txt file to save sentences containing the target.
        wait_time: Time (seconds) to wait for the page to load (int)
        debug: If True, prints a snippet of page source for inspection (bool)

    Returns:
        list of sentences containing target (list)
    """
    try:
        print(f"[INFO] Crawler started for {url}")

        # Start browser (Chrome headless)
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  
        options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        driver.get(url)

        # Wait until body is loaded
        WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # Capture all visible text
        text = driver.find_element(By.TAG_NAME, "body").text

        if debug:
            print("[DEBUG] First 500 chars of page source:")
            print(driver.page_source[:500])

        driver.quit()

        # Normalize spaces
        text = re.sub(r'\s+', ' ', text).strip()

        # Split by lines instead of punctuation (more reliable)
        lines = text.split("\n")

        # Filter and clean
        target_sentences = [line.strip() for line in lines if target.lower() in line.lower()]

        print(f"[INFO] Found {len(target_sentences)} sentences containing '{target}'.")

        with open(save_file_path, 'w', encoding='utf-8') as f:
            for sentence in target_sentences:
                f.write(sentence + '\n')

        return target_sentences

    except Exception as e:
        print(f"[ERROR] Crawler failed for {url}: {e}")
        return []


def load_patterns(file_path: str) -> list:
    """Read URL patterns from a txt file, ignoring comments (#) and empty lines"""
    if not os.path.exists(file_path):
        print(f"[ERROR] Pattern file not found: {file_path}")
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        return [
            line.strip()
            for line in f
            if line.strip() and not line.strip().startswith("#")
        ]


def multi_page_search(target: str, search_patterns: list, page_limit: int = 1, wait_time: int = 5) -> list:
    """
    Search multiple pages using the crawler (Selenium) and aggregate results.
    """
    all_results = []

    for pattern in search_patterns:
        for page in range(1, page_limit + 1):
            url = pattern.format(target=target, page=page)
            print(f"[INFO] Crawling URL: {url}")

            temp_file = f"temp_{target}_page_{page}.txt"

            try:
                results = crawler(url, target, temp_file, wait_time=wait_time)
                all_results.extend(results)
            except Exception as e:
                print(f"[WARNING] Skipping URL due to error: {url} | {e}")
                continue  

    return all_results