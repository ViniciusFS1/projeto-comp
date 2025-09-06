from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re
import time

def crawler(url: str, target: str, save_file_path: str, wait_time: int = 5) -> list:
    """
    Crawler usando Selenium.

    Args:
        url: Target website to be analyzed by the crawler (str)
        target: Desired word or sentence to be located (str)
        save_file_path: Path to the .txt file to save sentences containing the target.
        wait_time: Tempo (segundos) para esperar o carregamento da página (int)

    Returns:
        list of sentences containing target (list)
    """
    try:
        print("[INFO] Crawler has started operating")

        # Inicia navegador (Chrome headless)
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  
        options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        driver.get(url)
        time.sleep(wait_time)  # espera o carregamento

        # Captura todo o texto visível
        text = driver.find_element(By.TAG_NAME, "body").text

        driver.quit()

        # Normaliza espaços
        text = re.sub(r'\s+', ' ', text).strip()

        # Divide em sentenças
        sentences = re.split(r'[.!?]', text)

        # Filtra e limpa
        target_sentences = [sentence.strip() for sentence in sentences if target.lower() in sentence.lower()]

        print("[INFO] Crawler has located the target sentences.")

        with open(save_file_path, 'w', encoding='utf-8') as f:
            for sentence in target_sentences:
                f.write(sentence + '\n')

        print("[INFO] Crawler has finished.")
        return target_sentences

    except Exception as e:
        print(f"[ERROR] Crawler was unable to operate: {e}")
        return []


def multi_page_search(target: str, search_patterns: list, page_limit: int = 1, wait_time: int = 5) -> list:
    """
    Search multiple pages using the crawler (Selenium) and aggregate results.

    Args:
        target: The target word or phrase to search for (str)
        search_patterns: A list of URL patterns with placeholders {target} and {page}, e.g.,
                         "https://twitter.com/search?q={target}&f=live&page={}" (list)
        page_limit: Maximum number of pages to search per pattern (int)
        wait_time: Tempo (segundos) para esperar o carregamento da página (int)

    Returns:
        A combined list of sentences containing the target from all pages (list)
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
                print(f"[WARNING] Skipping URL due to crawler error: {url} | Error: {e}")
                continue  

    return all_results