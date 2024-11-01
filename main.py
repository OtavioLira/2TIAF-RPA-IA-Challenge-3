import time
import pandas as pd
import re
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import google.generativeai as genai
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

genai.configure(api_key="API_KEY")

model = genai.GenerativeModel('gemini-1.5-flash')

def generate_report(df):
    # Relatório de Estatísticas Descritivas
    print("Relatório de Estatísticas Descritivas")
    print(df.describe(include='all'))
    
    # Quantidade de vagas por empresa
    vagas_por_empresa = df['empresa'].value_counts()
    print("\nQuantidade de Vagas por Empresa:\n", vagas_por_empresa)
    
    # Faixa salarial
    print("\nAnálise de Salários:")
    print(df['salario'].describe())
    
    # Gráficos
    plt.figure(figsize=(10, 6))
    sns.countplot(y=df['empresa'], order=vagas_por_empresa.index)
    plt.title("Quantidade de Vagas por Empresa")
    plt.show()

    plt.figure(figsize=(10, 6))
    sns.barplot(df['salario'].dropna())
    plt.title("Distribuição de Salários")
    plt.show() 

def generate_insights(df):
    insights = ""

    # Resumo do dataset
    vagas_totais = df.shape[0]
    insights += f"Total de vagas encontradas: {vagas_totais}\n"

    # Empresa com mais vagas
    empresa_top = df['empresa'].value_counts().idxmax()
    vagas_empresa_top = df['empresa'].value_counts().max()
    insights += f"A empresa com mais vagas é {empresa_top}, com {vagas_empresa_top} vagas.\n"

    # Faixa salarial mais comum
    salario_medio = df['salario'].mean()
    insights += f"O salário médio das vagas é de R$ {salario_medio:.2f}.\n"

    # Enviando os insights para a API Gemini para enriquecer as análises
    response = model.generate_content(
        f"Baseado nos seguintes insights:\n\n{insights}\n\nQuais conclusões adicionais podemos tirar deste cenário de vagas e salários?"
    )

    insights += f"Insights fornecidos pela IA Gemini:\n{response.text}\n"

    print(insights)
    return insights


def clean_salary_column(df):
    # Preenchendo valores NaN com string vazia para evitar erros
    df['salario'] = df['salario'].fillna('').astype(str)

    # Remover tudo que não é número, substituindo por 0
    df['salario'] = df['salario'].str.replace(r'[^0-9]', '', regex=True)  # Mantém apenas dígitos
    df['salario'] = df['salario'].replace('', '0')  # Substitui strings vazias por '0'

    # Converte para float, substituindo valores não numéricos por 0
    df['salario'] = pd.to_numeric(df['salario'], errors='coerce').fillna(0)

    return df

def remove_special_chars(text):
    return re.sub(r'[^\w\s]', '', text)

def safe_find_element(driver, xpath):
    try:
        return driver.find_element(By.XPATH, xpath).text
    except Exception:
        return "não encontrado"

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
                nome_vaga = safe_find_element(driver, webpage["elementos_vaga"]["nome"]["xpath"])
                empresa_vaga = safe_find_element(driver, webpage["elementos_vaga"]["empresa"]["xpath"]) 
                descricao_vaga = safe_find_element(driver, webpage["elementos_vaga"]["descricao"]["xpath"])
                salario_vaga = safe_find_element(driver, webpage["elementos_vaga"]["salario"]["xpath"])
                localizacao_vaga = safe_find_element(driver, webpage["elementos_vaga"]["localizacao"]["xpath"])

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
    
    dataset_vagas = clean_salary_column(dataset_vagas)

    dataset_vagas.to_excel("Vagas-Catho.xlsx", engine='xlsxwriter')

    generate_report(dataset_vagas)
    generate_insights(dataset_vagas)
try:
    process()
except Exception as err:
    print(f"Erro, {err}")
finally:
    print("------Fim do processo-----")