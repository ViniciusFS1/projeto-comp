from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def crawler_reclameaqui(company: str, page_limit: int = 1, wait_time: int = 5) -> list:
    """
    Crawler específico para ReclameAqui.
    
    Args:
        company: Nome da empresa na URL (str), ex: "empresa-exemplo"
        page_limit: Número de páginas a buscar (int)
        wait_time: Tempo para esperar o carregamento da página (int)
    
    Returns:
        Lista de reclamações (list of str)
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # roda sem abrir janela
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    all_complaints = []
    
    for page in range(1, page_limit + 1):
        url = f"https://www.reclameaqui.com.br/empresa/{company}/reclamacoes/?pagina={page}"
        print(f"[INFO] Crawling {url}")
        driver.get(url)
        
        try:
            # Espera até que pelo menos uma reclamação seja carregada
            WebDriverWait(driver, wait_time).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.sc-1pe7b5t-0"))
            )
        except:
            print(f"[WARNING] Nenhuma reclamação carregada na página {page}")
            continue
        
        # Pega todos os blocos de reclamação
        complaints = driver.find_elements(By.CSS_SELECTOR, "div.sc-1pe7b5t-0")
        for c in complaints:
            text = c.text.strip()
            if text:
                all_complaints.append(text)
        
        # Pequena pausa para não sobrecarregar
        time.sleep(1)
    
    driver.quit()
    return all_complaints


if __name__ == "__main__":
    company_name = "Santander"  # substituir pelo nome da empresa na URL
    complaints = crawler_reclameaqui(company_name, page_limit=2)
    
    print(f"\n[RESULTS] Total de reclamações: {len(complaints)}\n")
    for idx, c in enumerate(complaints, 1):
        print(f"{idx}. {c}\n")