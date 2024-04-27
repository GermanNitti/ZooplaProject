import csv
from undetected_chromedriver import Chrome, ChromeOptions
from bs4 import BeautifulSoup
import time

def fetch_data(url):
    driver_path = '/path/to/chromedriver'  # Ruta completa al ejecutable del controlador de Chrome
    options = ChromeOptions()
    driver = Chrome(executable_path=driver_path, options=options)
    url_list = []

    try:
        driver.get(url)
         # Espera para que se cargue el contenido

        # Obtener el HTML de la página cargada
        html = driver.page_source

        # Crear un objeto BeautifulSoup para analizar el HTML
        soup = BeautifulSoup(html, 'html.parser')

        # Encuentra los elementos 'a' con los atributos especificados
        url_links = soup.find_all('div', class_='_14bi3x31n')  # Cambia 'tu_clase_div' por la clase real de tu div
        for div in url_links:
            links = div.find_all('a', {'aria-live': 'polite', 'class': 'qimhss0 qimhss4 qimhss9 _194zg6t8', 'href': True})  # Cambia 'tu_clase_ul' por la clase real de tu ul
            for link in links:
                full_url = "https://www.zoopla.co.uk" + link['href']
                url_list.append(full_url)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        driver.quit()

    return url_list

# Uso del ejemplo
url_to_scrape = "https://www.zoopla.co.uk/find-agents/branch/chancellors-amersham-amersham-10487/"
url_list = fetch_data(url_to_scrape)

# Imprimir la lista de URLs
for url in url_list:
    print(url)
