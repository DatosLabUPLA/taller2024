import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
now = datetime.now()

# Extracción del HTML de la pagina con request
url = 'https://www.t13.cl/etiqueta/region-metropolitana'
resultado = requests.get(url)
contenido = resultado.text
soup = BeautifulSoup(contenido, 'html.parser')
#soup = BeautifulSoup(contenido, 'lxml')
#print(soup.prettify())

lista_url = []
datos = pd.DataFrame(columns=['Titulo', 'Autores', 'Resumen', 'Fecha', 'Etiquetas', 'URL'])
# Extracción de url de todas la noticias más recientes de la RM
for i in soup.find_all('a', href=True):
    if i['href'].startswith('https://www.t13.cl/noticia/'): # Extraer solo los url de las noticias (Evitando CSS, templates, img, etc.)
        if i['href'] not in lista_url: # Evitar url duplicados
            lista_url.append(i['href'])
            resultado = requests.get(i['href'])
            contenido = resultado.text
            soup = BeautifulSoup(contenido, 'html.parser')
            #soup = BeautifulSoup(contenido, 'lxml')
            titulo = soup.find('h1')
            autores = soup.find('div', class_='autor')
            resumen = soup.find('div', class_='bajada')
            fecha = soup.find('time', class_='fecha')
            etiquetas_temp1 = soup.find('div', class_='articulo-categorias')
            etiquetas_temp2 = etiquetas_temp1.find_all('a')
            etiquetas = [etiqueta.text.strip() for etiqueta in etiquetas_temp2]
            noticia = [titulo.get_text(strip=True), autores.get_text(strip=True), resumen.get_text(strip=True), fecha.text, etiquetas, i['href']]
            datos.loc[len(datos)] = noticia

# Crear directorios si no existen
fechaActual = now.strftime('%Y%m%d') # Formato AAMMDD
try:
    os.makedirs(f'DATA/{fechaActual}')
except FileExistsError:
    pass
# Exportar DataFrame a CSV
with open(f'DATA/{fechaActual}/noticias.csv', 'w', newline='') as csvfile:
    datos.to_csv(csvfile, index=False)

# Archivo .log
with open('registro.log', 'a') as archivo_log:
    archivo_log.write(f'{str(now)} - {len(lista_url)} Noticias extraidas con exito - La información se extrajo del sitio web: https://www.t13.cl/etiqueta/region-metropolitana\n')

print('Fin del proceso')
print('Total de noticias extraídas: %s' % len(lista_url))