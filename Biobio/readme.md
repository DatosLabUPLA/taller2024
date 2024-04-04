# Municipalidad de Biobío

Este proyecto consiste en un scraper para recopilar información del sitio web de la Municipalidades del Biobío.

## Información General del Sitio

Sitio web de las Municipalidades del Biobío, proporcionan información sobre servicios municipales, noticias locales, eventos, y más.

## Estudiante Asignado

- **Nombre:** Jose Rene Meza Villalon

## Diccionario de Datos

A continuación se presenta un diccionario de datos para la base de datos generada por el scraper:

- **id:** Identificador único de la entrada en la base de datos.
- **link:** Enlace URL encontrado en el sitio web.
- **document_type:** Tipo de documento encontrado en el enlace (por ejemplo, "Link" para enlaces web, "Documento" para documentos descargables).
- **timestamp:** Fecha y hora en que se realizó la inserción en la base de datos.

## Librerías Utilizadas

El proyecto hace uso de las siguientes librerías de Python:

- BeautifulSoup
- requests
- sqlite3
- datetime
- urllib.parse
- collections
