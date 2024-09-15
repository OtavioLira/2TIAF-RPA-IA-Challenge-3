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
url = "https://www.catho.com.br/"

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
    driver.get(url)

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
        # # Percorrer por 10 paginas
        for i in range(10):
            print(f"Encontrado {len(lista_vagas)} vagas.")
            for vaga in lista_vagas:
                vaga = vaga.text.split("\n")

                # Raspagem de informações
                nome_vaga = vaga[0]
                empresa_vaga = vaga[1]
                descricao_vaga = vaga[2]
                salario_vaga = vaga[3]
                localizacao_vaga = vaga[4]

                nova_linha = pd.DataFrame([{
                    "nome": nome_vaga,
                    "empresa": empresa_vaga,
                    "descricao": descricao_vaga,
                    "salario": salario_vaga,
                    "vaga": localizacao_vaga
                }])

                dataset_vagas = pd.concat([dataset_vagas, nova_linha], ignore_index=True)
        
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Aceitar cookies apenas uma vez
            if not cookies_aceito:
                try:
                    cookies = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'acceptAll widget-policy-button widget-policy-button--blue')]"))
                    )
                    cookies.click()
                    cookies_aceito = True
                except:
                    print("Botão de cookies não encontrado ou já aceito anteriormente.")
            # Clicar no botão "Próximo"
            try:
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'ActionButton') and text()='Próximo']"))
                )
                next_button.click()
                time.sleep(5)  # Aguarda a próxima página carregar
            except:
                print("Botão 'Próximo' não encontrado ou não é mais clicável. Encerrando.")
                break  # Encerra o loop se o botão 'Próximo' não for encontrado
except Exception as err:
    print(f"Erro, {err}")
finally:
    dataset_vagas.to_excel("Vagas-Catho.xlsx")
    driver.quit()
