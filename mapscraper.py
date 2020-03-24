import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
os.chdir("/Users/canzonettaclaudio/Documents/LUCA CODING/Immobiliare")

page = requests.get('https://www.immobiliare.it/ricerca-mappa/Roma,RM/zona_10161/#/latitudine_41.94816/longitudine_12.54471/idTipologia_63/idContratto_1/idCategoria_2/sottotipologia_79/idMacrozonaGis_10161/zoom_14/pag_1')
contents = page.content
soup = BeautifulSoup(contents, 'html.parser')
listings = soup.find_all('div', class_ ='riga_annuncio')   
