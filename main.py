from selenium import webdriver
from selenium.webdriver.common import by
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
import time

#from selenium.webdriver.chrome.service import Service
#from webdriver_manager.chrome import ChromeDriverManager
#from selenium.webdriver.chrome.options import Options
 
driver = webdriver.Chrome()
url = "https://google.com"
try:
    driver.get(url)
    time.sleep(5)
except:
    print("Erro, não foi possível abrir o navegador")
finally:
    driver.quit()