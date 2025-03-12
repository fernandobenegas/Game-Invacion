import bs4
import requests

resultado = requests.get('https://escueladirecta.com/')


sopa = bs4.BeautifulSoup(resultado.text,'lxml')
columna_lateral = sopa.select('#block-13716409') # Seleccionamos la etiqueta la claase o el Id del lo que queremos extraer
for div in columna_lateral:
    print(div.getText()) #Con get text obtenemos solamente el texto sin la etiqueta