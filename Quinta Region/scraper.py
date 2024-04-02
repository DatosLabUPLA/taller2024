import requests
from bs4 import BeautifulSoup
import re

# Parte 1, obtener el HTML.

web = "https://store.steampowered.com/search/?filter=topsellers"
pedido = requests.get(web)
html = pedido.text


# Parte 2, "Parsear" el HTML.


soup = BeautifulSoup(html, "html.parser")


#Parte 3, Obtener los datos necesarios.


div_completo = soup.find_all('div', class_ = "col search_name ellipsis")

# fecha lanzamiento: col search_released responsive_secondrow
# precio: col search_price_discount_combined responsive_secondrow

producto = []
lanzamiento = []
precio = []

for div in div_completo:
    producto.append(div.text.strip())

print(producto)





