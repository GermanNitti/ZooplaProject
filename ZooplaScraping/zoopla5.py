from undetected_chromedriver import Chrome, ChromeOptions
from bs4 import BeautifulSoup
import csv
import time

def fetch_data(url):
    driver_path = '/home/german/Documentos/Work'
    options = ChromeOptions()
    driver = Chrome(executable_path=driver_path, options=options)

    try:
        driver.get(url)
        time.sleep(5)  # Espera para que se cargue el contenido

        # Obtener el HTML de la página cargada
        html = driver.page_source

        # Crear un objeto BeautifulSoup para analizar el HTML
        soup = BeautifulSoup(html, 'html.parser')

        # Encuentra los elementos 'ul' con la clase especificada
        uls = soup.find_all('ul', class_='listing-results clearfix js-gtm-list')

        # Crear una lista para almacenar URLs únicas
        unique_urls = []

        for ul in uls:
            # Encuentra los elementos 'li' dentro de cada 'ul'
            lis = ul.find_all('li')
            for li in lis:
                # Encuentra los elementos 'a' dentro de cada 'li'
                links = li.find_all('a', href=True)
                for link in links:
                    full_url = "https://www.zoopla.co.uk" + link['href']
                    unique_urls.append(full_url)

        return unique_urls

    except Exception as e:
        print(f"Error al procesar la URL {url}: {e}")
        return []

    finally:
        driver.quit()

# Uso del ejemplo
base_url = "https://www.zoopla.co.uk/for-sale/branch/chancellors-amersham-amersham-10487/?page_size=100&pn="
all_urls = []
page_number = 1
while True:
    url_to_scrape = base_url + str(page_number)
    print(f"Scrapeando página: {url_to_scrape}")  # Imprimir la página actual
    urls_on_page = fetch_data(url_to_scrape)
    if not urls_on_page:
        break
    all_urls.extend(urls_on_page)
    page_number += 1
    time.sleep(1)

# Escribir todas las URLs scrapeadas en un archivo CSV
with open('Zoopla5.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['URL'])
    for url in all_urls:
        writer.writerow([url])

print("¡Proceso completado! Las URLs se han guardado en ZooplaUrls.csv")
