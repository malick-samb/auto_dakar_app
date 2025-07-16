
# importer les packages
import pandas as pd
from requests import get # récupérer le code html de la page
from bs4 import BeautifulSoup as bs  # stocker le code html dans un object beautifulsoup
import time
import re

def scrape_auto(category, nb_pages):
    all_data = []

    for p in range(1, nb_pages + 1):
        url = f'https://dakar-auto.com/senegal/{category}?&page={p}'
        print(f"Scraping page: {url}")
        code_html = get(url,timeout=10)
        soup = bs(code_html.content, 'html.parser')
        containers = soup.find_all('div', class_='listings-cards__list-item mb-md-3 mb-3')

        for container in containers:
          try:
            url_container = 'https://dakar-auto.com' +  container.find('a',class_="listing-card__aside__inner d-block")['href']
            hc_container = get(url_container)
            soup_container = bs(hc_container.content, 'html.parser')
            marque = re.split(r'\s\d{4}\b', soup_container.find('h1', class_='listing-item__title').span.text.strip())[0].strip()
            price = soup_container.find('h4', class_='listing-item__price font-weight-bold text-uppercase mb-2').text.strip()
            province = soup_container.find('span', class_='province font-weight-bold d-inline-block').text.strip()
            nom = soup_container.find('h4', class_='listing-item-sidebar__author-name').text.strip()
            ul_tag = soup_container.find('ul', class_='listing-item__attribute-list list-inline')
            if ul_tag:
                li_tags = ul_tag.find_all('li', class_='listing-item__attribute list-inline-item')
                lines = [li.get_text(strip=True) for li in li_tags]

                kilometrage = lines[0] if len(lines) > 0 else None
                annee = lines[1].split(':')[-1].strip() if len(lines) > 1 else None
                boite = lines[2] if len(lines) > 2 else None
                carburant = lines[3] if len(lines) > 3 else None
            else:
                kilometrage = annee = boite =carburant= None

            if category.startswith("motos-and-scooters"):
                boite = None
                carburant = None

            if category.startswith("location-de-voitures"):
                kilometrage = None
                boite = None
                carburant = None

            dic = {
                'Marque de Voiture': marque,
                'Année': annee,
                'Prix': price,
                'Adresse': province,
                'Propriétaire': nom,
            }

            if not category.startswith("location-de-voitures"):
                dic['Kilométrage'] = kilometrage

            if category.startswith("voitures"):
                dic['Boîte de vitesse'] = boite
                dic['Carburant'] = carburant
                
            all_data.append(dic)
            time.sleep(0.5)
          except Exception as e:
            print(f"Erreur sur annonce: {e}")
            continue

    return pd.DataFrame(all_data)




