import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def scrapear_pagina(pagina_web):
    print("Abriendo el navegador Chrome")

    # Configuración de opciones para Chrome
    opciones = webdriver.ChromeOptions()

    # Usar ChromeDriverManager para obtener automáticamente el path del driver
    service = Service(ChromeDriverManager().install())

    # Iniciar el driver usando el servicio y las opciones
    driver = webdriver.Chrome(service=service, options=opciones)

    try:
        driver.get(pagina_web)
        print("Página cargada ...")
        html = driver.page_source
        return html
    finally:
        driver.quit()


def extraer_html(contenido_html):
    soup = BeautifulSoup(contenido_html,"html.parser")
    contenido_de_body = soup.body
    if contenido_de_body:
        return str(contenido_de_body)
    return""

def limpiar_body (contenido_body):
    soup = BeautifulSoup(contenido_body,"html.parser")

    for script_o_estilo in soup(["script", "style"]):
        script_o_estilo.extract()
 
    contenido_limpio = soup.get_text(separator="\n")

    contenido_limpio= "\n".join(
        line.strip() for line in contenido_limpio.splitlines() if line.strip()
    )
    return contenido_limpio
    

# Funcion para poder enviar los archivos al llm al limitar su cantidad de caracteres.

def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]