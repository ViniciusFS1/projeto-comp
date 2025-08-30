import requests
from bs4 import BeautifulSoup
import re
import os


url = "https://github.com/"  
target = "github"

save_file_path = os.path.abspath("crawler_processed_data.txt")

import requests
from bs4 import BeautifulSoup
import re

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
        print("[UPDATE] Crawler has started operating")
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

        print("[UPDATE] Crawler has located the target sentences.")

        with open(save_file_path, 'w', encoding='utf-8') as f:
            for sentence in target_sentences:
                f.write(sentence + '\n')

        return target_sentences

    except Exception as e:
        print(f"[ERROR] Crawler was unable to operate: {e}")
        return []