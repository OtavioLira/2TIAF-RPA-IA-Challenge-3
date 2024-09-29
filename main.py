from selenium import webdriver
from selenium.webdriver.common.by import By
#from selenium.webdriver.firefox.service import Service
#from webdriver_manager.firefox import GeckoDriverManager
#from selenium.webdriver.firefox.options import Options
#from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

import time
import pandas as pd
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


driver = webdriver.Chrome()
url_catho = "https://www.catho.com.br/"
url_gupy = "https://portal.gupy.io/"

dataset_vagas = {
    "nome": [],
    "empresa": [],
    "descricao": [],
    "salario": [],
    "vaga": []
}

dataset_vagas = pd.DataFrame(dataset_vagas)

cookies_aceito = False

try:
    # Abrindo o navegador
    driver.get(url_catho)

    # Pesquisando vaga
    input_vaga = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )

    input_vaga.send_keys("Estágio")
    input_vaga.submit()

    # Procurando lista de vsagas
    time.sleep(5)
    lista_vagas = driver.find_elements(By.XPATH, "//ul[contains(@class, 'gtm-class search-result-custom_jobList')]/li")

    # Verificando se sencontrou vagass
    if lista_vagas:
        print(f"Encontrado {len(lista_vagas)} vagas na Catho.")
        link_vagas = []
        for vaga in lista_vagas:
            link_vagas.append(vaga.find_element(By.XPATH,".//div[contains(@class, 'sc-bpUBKd sTalA')]//a").get_property("href"))
        for link in link_vagas:
            # Abrindo o navegador
            driver.get(link)

            # Raspagem de informaçõesss
            nome_vaga = driver.find_element(By.XPATH,"//header[contains(@class, 'Header-module')]//h1").text
            empresa_vaga = driver.find_element(By.XPATH,".//div[contains(@class, 'info-item')]").text
            descricao_vaga = driver.find_element(By.XPATH, ".//div[contains(@class, 'job-description')]").text
            salario_vaga = driver.find_element(By.XPATH,".//article[contains(@id, 'job')]//ul//li").text
            localizacao_vaga = driver.find_element(By.XPATH,".//div[contains(@class, 'cidades')]//button/a").text

            nova_linha = pd.DataFrame([{
                "nome": nome_vaga,
                "empresa": empresa_vaga,
                "descricao": descricao_vaga, 
                "salario": salario_vaga,
                "vaga": localizacao_vaga
            }])

            dataset_vagas = pd.concat([dataset_vagas,nova_linha], ignore_index=True)
        # codigo para continuar para outras paginas (não consegui fazer)
except Exception as err:
    print(f"Erro, {err}")

try:
    # Abrindo o navegador
    driver.get(url_gupy)

    # Pesquisando vaga
    input_vaga = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "searchTerm"))
    )

    input_vaga.send_keys("Programador Junior")
    input_vaga.submit()

    # Procurando lista de vsagas
    time.sleep(5)
    lista_vagas = driver.find_elements(By.XPATH, "//ul[contains(@class,'sc-a01de6b')]/li")

    # Verificando se sencontrou vagass
    if lista_vagas:
        print(f"Encontrado {len(lista_vagas)} vagas na GUPY.")
        link_vagas = []
        empresa_vagas = []
        for vaga in lista_vagas:
            link_vagas.append(vaga.find_element(By.XPATH,".//a[contains(@class, 'sc-4d881605-1 IKqnq')]").get_property("href"))
            empresa_vagas.append(driver.find_element(By.XPATH, "//p[contains(@class, 'sc-bBXxYQ eJcDNr sc-4d881605-5 bpsGtj')]").text)
        for i in range(len(link_vagas)):
            # Ir para pagina da vaga
            driver.get(link_vagas[i])
            time.sleep(5)

            # Raspagem de informações
            nome_vaga = driver.find_element(By.XPATH, "//h1[contains(@class, 'sc-ccd5d36-6 gdqSpl')]").text
            descricao_vaga = driver.find_element(By.CSS_SELECTOR, 'body > div > div > main > div > section > div > div > p').text
            salario_vaga = '-'
            localizacao_vaga = driver.find_element(By.XPATH, "//span[contains(@class, 'sc-dfd42894-0 bzQMFp')]").text
            
            nova_linha = pd.DataFrame([{
                "nome": nome_vaga,
                "empresa": empresa_vagas[i],
                "descricao": descricao_vaga,
                "salario": salario_vaga,
                "vaga": localizacao_vaga
            }])

            dataset_vagas = pd.concat([dataset_vagas,nova_linha], ignore_index=True)
except Exception as err:
    print(f"Erro, {err}")

dataset_vagas.to_excel("Vagas-Catho.xlsx")
driver.quit()
