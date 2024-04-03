#!/usr/bin/env python
# coding: utf-8

# Scraper

# In[ ]:


import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin
import sqlite3
from collections import deque

# Función para inicializar la base de datos
def initialize_database():
    conn = sqlite3.connect('scraped_data.db')
    c = conn.cursor()
    # Crear tabla para almacenar los datos
    c.execute('''CREATE TABLE IF NOT EXISTS scraped_data
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, link TEXT, document_type TEXT)''')
    conn.commit()
    conn.close()

# Función para insertar datos en la base de datos
def insert_data(link, document_type):
    conn = sqlite3.connect('scraped_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO scraped_data (link, document_type) VALUES (?, ?)", (link, document_type))
    conn.commit()
    conn.close()

# Función para registrar acciones en el archivo de log
def log_action(action):
    with open('scraper_log.log', 'a') as log:
        log.write(f'{datetime.now()}: {action}\n')

# Función para extraer la información y guardar en archivo
def scrape_and_save(url):
    # Conjunto para mantener un registro de los enlaces visitados
    visited_links = set()

    # Cola para gestionar los enlaces pendientes de visitar
    link_queue = deque([url])

    # Fecha y hora de inicio del scraping
    start_time = datetime.now()
    log_action(f'Iniciando scraping a las {start_time}')

    while link_queue:
        # Obtener el próximo enlace de la cola
        current_url = link_queue.popleft()

        # Realizar solicitud HTTP
        log_action(f'Obteniendo página: {current_url}')
        try:
            response = requests.get(current_url)
            response.raise_for_status()  # Lanzar una excepción si hay un error en la solicitud HTTP
        except requests.RequestException as e:
            log_action(f'Error al realizar la solicitud HTTP para {current_url}: {e}')
            continue

        if response.status_code == 200:
            # Marcar el enlace como visitado
            visited_links.add(current_url)

            # Analizar el HTML
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extraer los enlaces de la página
            log_action('Extrayendo enlaces de la página...')
            page_links = [urljoin(current_url, link['href']) for link in soup.find_all('a', href=True)]
            for page_link in page_links:
                if page_link not in visited_links and page_link not in link_queue and 'javascript:void(0)' not in page_link:
                    link_queue.append(page_link)
                    insert_data(page_link, 'Link')
                    log_action(f'Enlace encontrado: {page_link}')

            # Extraer los enlaces de los documentos (pdf, img, etc.)
            log_action('Extrayendo enlaces de documentos...')
            document_links = [urljoin(current_url, link['href']) for link in soup.find_all('a', href=True) if link['href'].endswith(('.pdf', '.jpg', '.png', '.doc', '.docx'))]
            for document_link in document_links:
                if document_link not in visited_links:
                    insert_data(document_link, 'Documento')
                    log_action(f'Documento encontrado: {document_link}')

        else:
            log_action(f'Error al realizar la solicitud HTTP para {current_url}')

    # Fecha y hora de finalización del scraping
    end_time = datetime.now()
    log_action(f'Scrape completado a las {end_time}')

    # Tiempo total de ejecución
    total_time = end_time - start_time
    log_action(f'Tiempo total de ejecución: {total_time}')

if __name__ == '__main__':
    # Inicializar la base de datos
    initialize_database()

    # URL de la página web semilla
    seed_url = 'https://munialtobiobio.cl/#'

    # Llamar a la función de scraping y guardar
    scrape_and_save(seed_url)


# In[ ]:




