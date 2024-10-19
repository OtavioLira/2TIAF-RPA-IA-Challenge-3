import time
import pandas as pd
import re
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def remove_special_chars(text):
    return re.sub(r'[^\w\s]', '', text)

def initial_config():
    webpages = []
    for fileConfig in os.listdir("config"):
        if fileConfig.endswith(".json"):
            full_path = os.path.join("config", fileConfig)
            with open(full_path, "r") as f:
                data = json.load(f)
                webpages.append(data)
    return webpages

def process():
    dataset_vagas = {
        "nome": [],
        "empresa": [],
        "descricao": [],
        "salario": [],
        "localizacao": [],
        "link vaga": []
    }

    dataset_vagas = pd.DataFrame(dataset_vagas)

    for webpage in initial_config():
        # Abrir página do site
        driver = webdriver.Chrome()
        driver.get(webpage["url"])

        #Pesquisando vaga
        input_vaga = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, webpage["pesquisa_vaga"]["xpath"]))
        )

        input_vaga.send_keys("Estágio")
        input_vaga.submit()

        time.sleep(5)
        
        # Descer página
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        #Pesquisar vagas
        lista_vagas = driver.find_elements(By.XPATH, webpage["lista_vagas"]["xpath"])

         # Verificando se sencontrou vagass
        if lista_vagas:
            print(f"Encontrado {len(lista_vagas)} vagas na {webpage['nome']}.")
            link_vagas = []
            for vaga in lista_vagas:
                link_vagas.append(vaga.find_element(By.XPATH, webpage["lista_vagas"]["xpath_link"]).get_property("href"))
            for link in link_vagas:
                # Abrindo o navegadors
                driver.get(link)

                # Raspagem de informaçõesss
                nome_vaga = driver.find_element(By.XPATH, webpage["elementos_vaga"]["nome"]["xpath"]).text
                empresa_vaga = driver.find_element(By.XPATH, webpage["elementos_vaga"]["empresa"]["xpath"]).text 
                descricao_vaga = driver.find_element(By.XPATH, webpage["elementos_vaga"]["descricao"]["xpath"]).text
                salario_vaga = driver.find_element(By.XPATH, webpage["elementos_vaga"]["salario"]["xpath"]).text
                localizacao_vaga = driver.find_element(By.XPATH, webpage["elementos_vaga"]["localizacao"]["xpath"]).text

                nova_linha = pd.DataFrame([{
                    "nome": nome_vaga,
                    "empresa": empresa_vaga,
                    "descricao": descricao_vaga, 
                    "salario": salario_vaga,
                    "localizacao": localizacao_vaga,
                    "link vaga": link
                }])

                dataset_vagas = pd.concat([dataset_vagas,nova_linha], ignore_index=True)
    driver.quit()

    # Aplicando a função para remover caracteres especiais
    dataset_vagas['descricao'] = dataset_vagas['descricao'].apply(remove_special_chars)
    dataset_vagas.to_excel("Vagas-Catho.xlsx")
try:
    process()
except Exception as err:
    print(f"Erro, {err}")
finally:
    print("------Fim do processo-----")