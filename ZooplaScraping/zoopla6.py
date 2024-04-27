from undetected_chromedriver import Chrome, ChromeOptions
from bs4 import BeautifulSoup
import csv
import time
import re

def fetch_data(url, all_urls):
    driver_path = '/path/to/chromedriver'  # Ruta completa al ejecutable del controlador de Chrome
    options = ChromeOptions()
    driver = Chrome(executable_path=driver_path, options=options)

    try:
        driver.get(url)
        time.sleep(1)  # Espera para que se cargue el contenido

        while True:
            # Obtener el HTML de la página cargada
            html = driver.page_source

            # Crear un objeto BeautifulSoup para analizar el HTML
            soup = BeautifulSoup(html, 'html.parser')

            # Encuentra los elementos 'div' con la clase 'agents-results'
            divs_results = soup.find_all('div', class_='agents-results')

            # Encuentra los elementos 'div' con la clase 'agents-results-branch clearfix' dentro de 'divs_results'
            for div_results in divs_results:
                divs_branches = div_results.find_all('div', class_='agents-results-branch clearfix')
                urls_found = False
                for div in divs_branches:
                    # Encuentra los elementos 'a' dentro de cada 'div'
                    links = div.find_all('a', href=True)
                    for link in links:
                        full_url = "https://www.zoopla.co.uk" + link['href']
                        if full_url.startswith("tel:"):
                            phone_number = re.sub(r'tel:\+', '', full_url)
                            all_urls.add(phone_number)  # Agrega el número de teléfono directamente
                            print(f"Teléfono: {phone_number}")
                            urls_found = True
                        elif full_url not in all_urls:
                            all_urls.add(full_url)
                            print(full_url)
                            urls_found = True

                if not urls_found:
                    break

            # Buscar y hacer clic en el enlace de siguiente página
            next_page_link = soup.find('div', class_='paginate bg-muted').find('a', class_='button paginator-btn-next', href=True)
            
            if next_page_link:
                next_page_url = "https://www.zoopla.co.uk" + next_page_link['href']
                driver.get(next_page_url)
                time.sleep(5)  # Espera para que se cargue el contenido
            else:
                break

        return True

    except Exception as e:
        print(f"Error: {e}")
        return False

    finally:
        driver.quit()

# Uso del ejemplo
base_url = "https://www.zoopla.co.uk/find-agents/company/chancellors-688/?page_size=100&pn="
all_urls = set()
page_number = 1
while True:
    url_to_scrape = base_url + str(page_number)
    print(f"Scrapeando página: {url_to_scrape}")  # Imprimir la página actual
    if not fetch_data(url_to_scrape, all_urls):
        break
    page_number += 1
    time.sleep(1)

# Guardar las URLs en un archivo CSV
with open('zoopla6.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['URL'])
    for url in all_urls:
        if url.startswith("tel:"):
            phone_number = re.sub(r'tel:\+', '', url)
            writer.writerow([phone_number])
        else:
            writer.writerow([url])
