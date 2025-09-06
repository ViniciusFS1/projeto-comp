#Importa as bibliotecas necessárias
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import datetime
import pandas as pd
import numpy as np
import openpyxl

#Define o caminho para o chromedriver
chromedriver = 'C:/Users/matheus.souza/Documents/Drivers/chromedriver'

#Instancia o Google Chrome
navegador = webdriver.Chrome(chromedriver)

#Seleciona a página desejada
navegador.get("https://www.reclameaqui.com.br/empresa/{}/".format('Insira o nome da empresa que completa o link'))

#Cria um intervalo de espera de 2 segundos
time.sleep(2)

#Localiza o botão para aceitar cookies e clica
navegador.find_element("xpath",'/html/body/div[2]/div[2]/a[1]').click()

#Rola a página 300 pixels para baixo, para que os alvos de cliques futuros não fiquem obstruídos
navegador.execute_script("window.scrollBy(0, 300)")

#Define os períodos de dados desejados e seus caminhos html
periodos = {'seis_meses':'//*[@id="reputation-tab-1"]',
           'doze_meses':'//*[@id="reputation-tab-2"]',
           'geral':'//*[@id="reputation-tab-5"]'
          }

#Define os elementos a serem coletados e seus caminhos html
elementos = {'nota_geral':'//*[@id="reputation"]/div[1]/div[1]/div[2]/span[2]/b',
            'num_reclamacoes':'//*[@id="reputation"]/div[1]/div[2]/a[1]/div/div/b',
            'num_respondidas':'//*[@id="reputation"]/div[1]/div[2]/a[2]/div/div/b',  
            'perc_recl_resp':'//*[@id="reputation"]/div[2]/div[1]/div[1]/span',
            'novam_negoc':'//*[@id="reputation"]/div[2]/div[1]/div[2]/span', 
            'indice_solucao':'//*[@id="reputation"]/div[2]/div[1]/div[3]/span',  
            'nota_consumidor':'//*[@id="reputation"]/div[2]/div[1]/div[4]/span'
           }

#Cria listas que conterão os dados de cada indicador
listas = {'nota_geral':[],            
          'num_reclamacoes':[],            
          'num_respondidas':[],              
          'perc_recl_resp':[],            
          'novam_negoc':[],             
          'indice_solucao':[],              
          'nota_consumidor':[]
         }

#Define o momento da coleta dos dados
agora = datetime.datetime.now()

#Percorre os períodos definidos
for periodo in periodos:
    #Cria um intervalo de espera de 1 segundo
    time.sleep(1)

    #Seleciona o período desejado localizando-o pelo 'xpath' e clicando
    navegador.find_element("xpath",periodos[periodo]).click()
    
    #Cria um intervalo de espera de 1 segundo
    time.sleep(1)
    
    #Percorre todos os elementos
    for elemento in elementos:
        #Localiza um elemento na página pelo 'xpath'
        element = navegador.find_element("xpath",elementos[elemento])

        #Extrai o texto do elemento localizado
        text = element.text

        #Adiciona o texto resultante à lista respectiva
        listas[elemento].append(text)
        
#Fecha o navegador
navegador.quit()

#Cria o dataframe que conterá os dados coletados de forma estruturada
df_resumo = pd.DataFrame(listas)
#Cria uma coluna com a data da coleta dos dados
df_resumo['data'] = agora.date()
#Cria uma coluna com a hora da coleta dos dados
df_resumo['hora'] = agora.time()
#Cria uma coluna que define a qual período pertence cada linha de dados do dataframe
periodos = ['Últimos 6 meses','Últimos 12 meses','Geral']
df_resumo['periodo'] = periodos
#Organiza as colunas do dataframe resultante
df_resumo = df_resumo.iloc[:,[7,8,9,0,1,2,3,4,5,6]]

#Instancia o arquivo xlsx que contém os registros históricos dos indicadores coletados (deve seguir a mesma estrutura do dataframe)
workbook = openpyxl.load_workbook('Insira o caminho do arquivo de registro aqui')

#Define a aba da planilha a ser editada
sheet = workbook.get_sheet_by_name('Insira aqui o nome da planilha que contém os registros')

#Determina o formato da coluna 'data'
df_resumo['data'] = df_resumo['data'].apply(lambda data: pd.to_datetime(data).date())
#Percorre as colunas que devem ser formatadas como float e o faz
for i in range(3,6):
    df_resumo.iloc[:,i] = df_resumo.iloc[:,i].astype(float)
#Percorre as colunas que devem ser formatadas como percentuais e o faz
for i in range(6,9):
    df_resumo.iloc[:,i] = df_resumo.iloc[:,i].apply(lambda num: float(num.replace('%',''))/100)
#Converte a coluna em float
df_resumo.iloc[:,9] = df_resumo.iloc[:,9].astype(float)
#Insere cada linha do dataframe no arquivo de regitros
for linha in df_resumo.values.tolist():
    sheet.append(linha)

#Salva as alterações realizadas
workbook.save('Insira o caminho do arquivo de registro aqui')