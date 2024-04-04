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
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, link TEXT, document_type TEXT, comuna TEXT)''')
    conn.commit()
    conn.close()

# Función para insertar datos en la base de datos
def insert_data(link, document_type, comuna):
    conn = sqlite3.connect('scraped_data.db')
    c = conn.cursor()
    # Verificar si el enlace ya existe en la base de datos
    c.execute("SELECT * FROM scraped_data WHERE link=?", (link,))
    if not c.fetchone():  # Si no hay coincidencias, insertar el enlace
        c.execute("INSERT INTO scraped_data (link, document_type, comuna) VALUES (?, ?, ?)", (link, document_type, comuna))
        conn.commit()
        print(f'Enlace insertado para la comuna "{comuna}": {link}')
    else:
        print(f'Enlace duplicado para la comuna "{comuna}": {link}')
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

    # Lista de comunas de la Región del Biobío
    comunas_biobio = [
        'alto-biobio', 'antuco', 'arauco', 'cabrero', 'cañete', 'chiguayante', 
        'concepcion', 'contulmo', 'coronel', 'coranilahue', 'florida', 'hualpen', 
        'hualqui', 'laja', 'lebu', 'los-alamos', 'los-angeles', 'lota', 'mulchen', 
        'nacimiento', 'negrete', 'penco', 'quilaco', 'quilleco', 'san-pedro-de-la-paz', 
        'san-rosendo', 'santa-barbara', 'santa-juana', 'talcahuano', 'tirua', 'tome', 
        'tucapel'
    ]

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
                # Verificar si el enlace contiene alguna comuna del Biobío
                for comuna in comunas_biobio:
                    if comuna in page_link.lower():
                        # Almacenar el enlace etiquetado por el tipo de documento y la comuna
                        insert_data(page_link, 'Link', comuna)

            # Buscar el botón de cambio de página y agregar su enlace a la cola
            next_page_button = soup.find('a', class_='next')
            if next_page_button:
                next_page_link = urljoin(current_url, next_page_button['href'])
                if next_page_link not in visited_links and next_page_link not in link_queue:
                    link_queue.append(next_page_link)
                    log_action(f'Agregado enlace de próxima página: {next_page_link}')

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
    seed_url = 'https://infomunicipalidades.com/biobio/'

    # Llamar a la función de scraping y guardar
    scrape_and_save(seed_url)


# In[ ]:




