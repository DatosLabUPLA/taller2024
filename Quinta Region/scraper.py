import requests

web = "https://www.portaltransparencia.cl/PortalPdT/directorio-de-organismos-regulados/?org=MU332"

result = requests.get(web)

conten = result.text

print(conten)
