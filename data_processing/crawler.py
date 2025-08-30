import requests
from bs4 import BeautifulSoup
import re
import os

def crawler(url: str, target: str, save_file_path: str) -> list:
    """
    Crawler

    Args:
        url: Target website to be analyzed by the crawler (str)
        target: Desired word or sentence to be located (str)
        save_file_path: Path to the .txt file to save sentences containing the target.

    Returns:
        list of sentences containing target (list)
    """
    try:
        print("[INFO] Crawler has started operating")
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text(separator=' ')

        # Normaliza espaços e quebras de linha
        text = re.sub(r'\s+', ' ', text).strip()

        # Divide em sentenças
        sentences = re.split(r'[.!?]', text)

        # Filtra e limpa espaços extras
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

def multi_page_search(target: str, search_patterns: list, page_limit: int = 1) -> list:
    """
    Search multiple pages using the crawler and aggregate results.

    Args:
        target: The target word or phrase to search for (str)
        search_patterns: A list of URL patterns with placeholders {target} and {page}, e.g.,
                         "https://twitter.com/search?q={target}&f=live&page={}" (list)
        page_limit: Maximum number of pages to search per pattern (int)

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
                results = crawler(url, target, temp_file)
                all_results.extend(results)
            except Exception as e:
                print(f"[WARNING] Skipping URL due to crawler error: {url} | Error: {e}")
                continue  

    return all_results