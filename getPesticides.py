from bs4 import BeautifulSoup
import requests
import csv

html_text = requests.get('https://www.gov.br/anvisa/pt-br/setorregulado/regularizacao/agrotoxicos/monografias/monografias-autorizadas-por-letra')
print('getting page ...')

soup = BeautifulSoup(html_text.text, "lxml")

ul_element = soup.find('ul', class_='toggable-content')

with open('pesticidasPermitidos.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    
    csv_writer.writerow(['Nome do pesticida no Brasil', 'Detalhes Anvisa'])

    ul_element = soup.find('ul', class_='toggable-content')

    if ul_element:
        anchor_elements = ul_element.find_all('a', href=lambda x: x and x.startswith("https://www.gov.br/anvisa/pt-br/setorregulado/regularizacao/agrotoxicos/monografias/monografias-autorizadas/"))
        for anchor in anchor_elements:
            if len(anchor.text) <= 6:
                continue
            print(anchor.text)
            csv_writer.writerow([anchor.text[6:], anchor['href']]) 
    else:
        csv_writer.writerow(["No <ul> element with class 'toggable-content' found.", ""])  