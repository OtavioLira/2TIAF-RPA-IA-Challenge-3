from selenium import webdriver
from selenium.webdriver.common.by import By
#from selenium.webdriver.firefox.service import Service
#from webdriver_manager.firefox import GeckoDriverManager
#from selenium.webdriver.firefox.options import Options
#from selenium.webdriver.firefox.service import Service as FirefoxService
import time
import pandas as pd

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
 
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

try:
    # Abrindo o navegador
    driver.get(url)

    time.sleep(5)

    # Pesquisando vaga
    input_vaga = driver.find_element(By.NAME, value="q")
    input_vaga.send_keys("Estágio")
    input_vaga.submit()

    # Procurando lista de vagas
    lista_vagas = driver.find_elements(By.XPATH, "//ul[contains(@class, 'gtm-class search-result-custom_jobList')]/li")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Verificando se encontrou vagas
    if lista_vagas:
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
    else:
        print("Nenhuma vaga encontrada.")

    time.sleep(5)
except Exception as ex:
    print(f"Erro, {ex}")
finally:
    print("Finalizando processo")
    print(dataset_vagas)
    driver.quit()