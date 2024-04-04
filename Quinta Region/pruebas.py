import requests
from bs4 import BeautifulSoup
from datetime import datetime                   #Libreria para saber hora y fecha del computador
import logging                                  #Libreria que nos ayuda con logs
from pathlib import Path                        #Libreria que nos ayuda con el directorio de carpeta
import sqlite3 as sql                           #Base de datos
import pandas as pd                             #DataFrames
import shutil                                   #Ayuda a mover archivos de directorio

# Configuramos el logging para que en consola nos arroje la informacion en nivel de INFO

logging.basicConfig(level = logging.INFO)


# Inicio de datetime para conocer fecha y hora de inicio del Scrap

inicio = datetime.now()

nombre_carpeta = inicio.strftime("%Y-%m-%d")

# Crear Carpeta data y subcarpeta

ruta_carpeta = Path('Data', nombre_carpeta)

if not ruta_carpeta.parent.is_dir():
    ruta_carpeta.parent.mkdir()

ruta_carpeta.mkdir(parents=True, exist_ok=True)


log_str = inicio.strftime('%Y-%m-%d_%H:%M')


# Inicio del programa

logging.info(" Hora de inicio: " + log_str + "\n")

with open("Data/" + nombre_carpeta + "/logs.txt", "a") as file_object:
    file_object.write("Hora y fecha de inicio: " + log_str + "\n")

url = "https://store.steampowered.com/search/?filter=topsellers&ndl=1"


# Obtenemos el html

logging.info(" Obteniendo el HTML. \n")

response = requests.get(url)

with open("Data/" + nombre_carpeta + "/logs.txt", "a") as file_object:
    file_object.write("Obteniendo HTML. \n")

# Parseo del HTML 

logging.info(" Parseando el HTML. \n")

soup = BeautifulSoup(response.content, "html.parser")

with open("Data/" + nombre_carpeta + "/logs.txt", "a") as file_object:
    file_object.write("Parseo de HTML.\n")

# Obtenemos los links de interés
    
logging.info(" Obteniendo links de interés. \n")

juegos = soup.find_all("a", class_="search_result_row")

with open("Data/" + nombre_carpeta + "/logs.txt", "a") as file_object:
    file_object.write("Obteniendo Links de interés. \n")


# Creamos listas que utilizaremos.
   
logging.info(" Creando listas de utilidad. \n")

with open("Data/" + nombre_carpeta + "/logs.txt", "a") as file_object:
    file_object.write("Creando listas de utilidad.\n")

nombres_juegos = []

fechas_lanzamiento = []

precios_juegos = []

desarrollador = []

editor = []



# Extraemos la información de cada juego

for juego in juegos:
    url_juego = juego["href"]

    response = requests.get(url_juego)
    soup_juego = BeautifulSoup(response.content, "html.parser")

    nombre_juego = soup_juego.find("div", class_="apphub_AppName")
    if nombre_juego:
        nombre_juego = nombre_juego.text.strip()
    else:
        nombre_juego = "Información no encontrada"
    
    logging.info(" Extrayendo informacion del juego : " + nombre_juego + ".\n")

    fecha_lanzamiento = soup_juego.find("div", class_="release_date")

    if fecha_lanzamiento:
        fecha_lanzamiento = fecha_lanzamiento.text.strip()
        
        # Buscar el índice del carácter de nueva línea
        indice_nueva_linea = fecha_lanzamiento.find("\n")
        
        if indice_nueva_linea != -1:
            # Obtener todo lo que viene después del carácter de nueva línea
            fecha_lanzamiento = fecha_lanzamiento[indice_nueva_linea + 1:].strip()
        else:
            print("No se encontró el carácter de nueva línea.")
    else:
        fecha_lanzamiento = "Información no encontrada"
        print(fecha_lanzamiento)


    precio_juego = soup_juego.find("div", class_="price")
    if precio_juego:
        precio_juego = precio_juego.text.strip()
    else:
        precio_juego = "0"
    
    desarrollador_contenedor = soup_juego.find("div", class_="dev_row")
    if desarrollador_contenedor:
        desarrollador_juego = desarrollador_contenedor.find("a").text.strip()
    else:
        desarrollador_juego = "Informacion no encontrada"

    editor_contenedor = soup.find("div", class_="dev_row")
    if editor_contenedor:
        editor_juego = editor_contenedor.find("a").text.strip()
    else:
        editor_juego = "Informacion no encontrada"

    with open("Data/" + nombre_carpeta + "/logs.txt", "a") as file_object:
        file_object.write("Extrayendo datos de interes del juego: " + nombre_juego + "\n")
    
    logging.info(" Añadiendo información a listas. \n")

    #Añadir todo a las listas correspondientes.

    nombres_juegos.append(nombre_juego)
    fechas_lanzamiento.append(fecha_lanzamiento)
    precios_juegos.append(precio_juego)
    desarrollador.append(desarrollador_juego)
    editor.append(editor_juego)

    with open("Data/" + nombre_carpeta + "/logs.txt", "a") as file_object:
        file_object.write("Iniciando siguiente juego.\n")
    logging.info(" Iniciando siguiente juego.\n")

fin = datetime.now()

log_str_fin = fin.strftime('%Y-%m-%d_%H:%M')




'''
nombre_db = "tarea.db"

conn = sql.connect(str(ruta_carpeta) + "/" + nombre_db)

cursor = conn.cursor()

cursor.execute(''CREATE TABLE IF NOT EXISTS datos(
               nombre TEXT, 
               desarrollador TEXT,
               editor TEXT,
               fecha_lanzamiento TEXT,
               precio TEXT) '')

for datos, desarrolladores, editores, fecha, precio in zip(nombres_juegos, desarrollador, editor, fechas_lanzamiento, precios_juegos):
    cursor.execute("INSERT INTO datos (nombre, desarrollador, editor, fecha_lanzamiento, precio) VALUES (?, ?, ?, ?, ?)",
                   (datos, desarrolladores, editores, fecha, precio))
    
conn.commit()

ultimo_id = cursor.lastrowid

if ultimo_id > 0:
    print(f"Registro insertado correctamente con ID: {ultimo_id}")
else:
    print("Error al insertar el registro")

conn.close()

'''
# Se unen las listas para crear el DataFrame

logging.info("Uniendo listas. \n")

with open("Data/" + nombre_carpeta + "/logs.txt", "a") as file_object:
    file_object.write("Uniendo listas.\n")

lista_completa = list(zip(nombres_juegos, desarrollador, editor, fechas_lanzamiento, precios_juegos))

logging.info("Creando dataFrame. \n")
with open("Data/" + nombre_carpeta + "/logs.txt", "a") as file_object:
    file_object.write("Creando DataFrame.\n")

# Definimos el nombre de las columnas para el DataFrame

columnas = ['Nombre juego', 'Desarrollador', 'Editor', 'Lanzamiento', 'Precio']

# Se crea el DataFrame

df = pd.DataFrame(lista_completa, columns = columnas)

logging.info("Creando base de datos. \n")
with open("Data/" + nombre_carpeta + "/logs.txt", "a") as file_object:
    file_object.write("Creando Base de datos.\n")

# Creamos la base de datos 

nombre_db = "tarea.db"

conn = sql.connect(str(ruta_carpeta) + "/" + nombre_db)

#Si la base de datos existe se reemplaza
df.to_sql( "datos", conn, if_exists = "replace")

logging.info("Creando CSV. \n")
with open("Data/" + nombre_carpeta + "/logs.txt", "a") as file_object:
    file_object.write("Creando CSV.\n")

#Se crea el CSV

df.to_csv("datos", index=False)

logging.info("Moviendo archivo de Directorio. \n")
with open("Data/" + nombre_carpeta + "/logs.txt", "a") as file_object:
    file_object.write("Moviendo archivo de Directorio.\n")

# Movemos el CSV a la carpeta indicada.
shutil.move("datos", ruta_carpeta)

logging.info("Traspaso completado. \n")

with open("Data/" + nombre_carpeta + "/logs.txt", "a") as file_object:
    file_object.write("Traspaso completado.\n")

logging.info(" Hora de termino: " + log_str_fin + "\n")
with open("Data/" + nombre_carpeta + "/logs.txt", "a") as file_object:
    file_object.write(" Hora de termino: " + log_str_fin + "\n")
