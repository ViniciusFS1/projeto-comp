from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import datetime
import os

# Caminho para o chromedriver
chromedriver_path = 'c:\\Users\\Lior Lerner\\Downloads\\chromedriver-win64\\chromedriver.exe'

# Configurações do Chrome
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-extensions")

# Inicializa o driver
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Acessa a página do Santander no Reclame Aqui
url = "https://www.reclameaqui.com.br/empresa/santander/"
driver.get(url)

# Aguarda o carregamento completo da página
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="reputation"]/div[1]/div[1]/div[2]/span[2]/b'))
)

# Coleta os dados
data = {
    'nota_geral': driver.find_element(By.XPATH, '//*[@id="reputation"]/div[1]/div[1]/div[2]/span[2]/b').text,
    'num_reclamacoes': driver.find_element(By.XPATH, '//*[@id="reputation"]/div[1]/div[2]/a[1]/div/div/b').text,
    'num_respondidas': driver.find_element(By.XPATH, '//*[@id="reputation"]/div[1]/div[2]/a[2]/div/div/b').text,
    'perc_recl_resp': driver.find_element(By.XPATH, '//*[@id="reputation"]/div[2]/div[1]/div[1]/span').text,
    'novas_negociacoes': driver.find_element(By.XPATH, '//*[@id="reputation"]/div[2]/div[1]/div[2]/span').text,
    'indice_solucao': driver.find_element(By.XPATH, '//*[@id="reputation"]/div[2]/div[1]/div[3]/span').text,
    'nota_consumidor': driver.find_element(By.XPATH, '//*[@id="reputation"]/div[2]/div[1]/div[4]/span').text,
    'data': datetime.datetime.now().date(),
    'hora': datetime.datetime.now().time(),
}

# Fecha o driver
driver.quit()

# Cria um DataFrame com os dados coletados
df = pd.DataFrame([data])

# Caminho do arquivo Excel
file_path = 'reclameaqui_santander.xlsx'

# Verifica se o arquivo existe
if os.path.exists(file_path):
    # Se existir, carrega o arquivo e adiciona os novos dados
    df_existing = pd.read_excel(file_path)
    df = pd.concat([df_existing, df], ignore_index=True)
    df.to_excel(file_path, index=False)
else:
    # Se não existir, cria um novo arquivo com os dados
    df.to_excel(file_path, index=False)

print(f"Dados salvos em {file_path}")
