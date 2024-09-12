from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
import time

#from selenium.webdriver.chrome.service import Service
#from webdriver_manager.chrome import ChromeDriverManager
#from selenium.webdriver.chrome.options import Options
 
driver = webdriver.Chrome()
url = "https://www.catho.com.br/"
Continue = False

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

    # Verificando se encontrou vagas
    if lista_vagas:
        print(f"Encontrado {len(lista_vagas)} vagas.")
        for vaga in lista_vagas:
            print("-"*10)
            print(vaga.text.split("\n"))  # Exibe o texto de cada vaga
            vaga = vaga.text.split("\n")

            # Raspagem de informações
            nome_vaga = vaga[0]
            empresa_vaga = vaga[1]
            descricao_vaga = vaga[2]
            salario_vaga = vaga[3]
            localizacao_vaga = vaga[4]

            print(f""" Sobre a vaga
            nome da vaga: {nome_vaga}
            empresa da vaga: {empresa_vaga}
            descricao da vaga: {descricao_vaga}
            salario da vaga: {salario_vaga}
            localização da vaga: {localizacao_vaga}
            """)

            print("-"*10)
    else:
        print("Nenhuma vaga encontrada.")

    time.sleep(5)
except Exception as ex:
    print(f"Erro, {ex}")
finally:
    print("Finalizando processo")
    driver.quit()