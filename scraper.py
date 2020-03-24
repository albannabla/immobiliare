import requests, os
from bs4 import BeautifulSoup
import pandas as pd
os.chdir("/Users/canzonettaclaudio/Documents/CODING/Immobiliare")

# determine number of pages
page = requests.get('https://www.immobiliare.it/Roma/vendita_immobili_commerciali/negozio_locale-Roma.html?criterio=rilevanza&pag=1&idMZona[]=10161')
contents = page.content
soup = BeautifulSoup(contents, 'html.parser')
tot_pages = len(soup.find('ul', class_ = 'pagination__number'))-2

# build url list
urls = []
for i in range(tot_pages):
    urls.append('https://www.immobiliare.it/Roma/vendita_immobili_commerciali/negozio_locale-Roma.html?criterio=rilevanza&pag='+str(i+1)+'&idMZona[]=10161')

#initialize lists
shopids = []
links = []
prices = []
titles = []
areas = []

# scrape all pages
for x in urls: 
    page = requests.get(x)
    contents = page.content
    soup = BeautifulSoup(contents, 'html.parser')
    listings = soup.find_all('li', class_ ='listing-item')    
    for shop in listings:
        if shop.ul is not None: 
            price = shop.ul.li.text
            prices.append(price)
            details = shop.find('sup')
            if details is not None:
                area = details.parent.span.text
            else:
                area = 0
            areas.append(area)    
            titdet = shop.find(class_ = 'descrizione__titolo')
            if titdet is not None:  
                title = titdet.text
                titles.append(title)
            else:
                titles.append("no description")
            link = shop.a['href']
            links.append(link)
            shopid = shop.a['id']
            shopids.append(shopid)

#build dataframe in pandas for visualization
test_df = pd.DataFrame({'id': shopids,
                        'link': links,
                        'price': prices,
                        'description': titles,
                        'area': areas
                        })

#clean up data
test_df['price'] = test_df['price'].str.replace(',', '')
test_df['price'] = test_df['price'].str.replace('.', '')
test_df['price'] = test_df['price'].str.replace('€', '')
test_df['price'] = test_df['price'].str.replace(' ', '')
test_df['price'] = test_df['price'].str.replace('\n', '')
test_df['area'] = test_df['area'].str.replace('.', '')


#export in excel 
test_df.to_excel("data.xlsx")

#print out text to confirm successful scraping 
print(test_df.info())



