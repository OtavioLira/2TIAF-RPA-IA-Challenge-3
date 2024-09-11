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

    # Procurando input de pesquisa
    input_vaga = driver.find_element(By.NAME, value="q")
    input_vaga.send_keys("Estágio")
    input_vaga.submit()

    # pesquisando vaga
    submit_button = driver.find_element(By.NAME, value="submit")
    submit_button.submit()

    time.sleep(5)
except Exception as ex:
    print(f"Erro, {ex}")
finally:
    print("Finalizando processo")
    #driver.quit()