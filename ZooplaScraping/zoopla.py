from undetected_chromedriver import Chrome, ChromeOptions
from bs4 import BeautifulSoup

from urllib.parse import urljoin

def fetch_data(url):
    driver_path = '/home/german/Documentos/Work'
    options = ChromeOptions()
    driver = Chrome(executable_path=driver_path, options=options)

    try:
        driver.get(url)
          # Espera para que se cargue el contenido

        # Obtener el HTML de la página cargada
        html = driver.page_source

        # Crear un objeto BeautifulSoup para analizar el HTML
        soup = BeautifulSoup(html, 'html.parser')

        # Encuentra los elementos 'a' con los atributos especificados
        url_links = soup.findAll('a', {'style': 'padding-left: 0;', 'class': 'btn-browse-row-clickable', 'href': True})

        # Crear una lista para almacenar los valores de href
        href_valores = []

        # Iterar sobre los elementos encontrados
        for link in url_links:
            # Obtener el valor del atributo href de cada elemento y agregarlo a la lista
            href_valor = link.get('href')
            if href_valor.startswith("tel:"):
                continue  # Si el enlace comienza con 'tel:', continuar con el siguiente enlace
            if not href_valor.startswith("http"):
                href_valor = "https://www.zoopla.co.uk" + href_valor
            href_valores.append(href_valor)

        # Devolver la lista de valores de href
        return href_valores

    except Exception as e:
        print(f"Error: {e}")

    finally:
        driver.quit()
        #------------------------------------------------

# URL inicial para obtener los enlaces de agentes inmobiliarios
url_to_scrape = "https://www.zoopla.co.uk/find-agents/estate-agents/"
enlaces = fetch_data(url_to_scrape)


def fetch_data_pages(enlaces):
    links2=[]
    driver_path = '/home/german/Documentos/Work'
    options = ChromeOptions()
    driver = Chrome(executable_path=driver_path, options=options)

    try:
        # Conjunto para almacenar las URLs únicas
        unique_links = set()

        for url in enlaces:
            driver.get(url)
             # Espera para que se cargue el contenido

            # Obtener el HTML de la página cargada
            html = driver.page_source

            # Crear un objeto BeautifulSoup para analizar el HTML
            soup = BeautifulSoup(html, 'html.parser')

            # Encuentra los elementos 'a' con los atributos especificados
            url_links = soup.findAll('a', href=True)

            # Agregar los enlaces únicos al conjunto
            for link in url_links:
                href_valor = link.get('href')
                if href_valor.startswith("tel:") or href_valor == "https://www.zoopla.co.uk/find-agents/estate-agents/":
                    continue  # Si el enlace comienza con 'tel:' o es igual al enlace base, continuar con el siguiente enlace
                if not href_valor.startswith("http"):
                    href_valor = "https://www.zoopla.co.uk" + href_valor
                if "find-agents/estate-agents/" in href_valor:
                    unique_links.add(href_valor)

        # Guardar los enlaces únicos en un archivo de texto
        with open("enlaces.txt", "w") as file:
            for link in unique_links:
                file.write(link + "\n")
                links2.append(link)
                print(link)

        return links2
    except Exception as e:
        print(f"Error: {e}")

    finally:
        driver.quit()

# Llamar a la función para obtener los enlaces de cada página
saranga=fetch_data_pages(enlaces[:1])

#------------------------------------------

def extract_data_from_page(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    li_elements = soup.find_all('li', class_='_1815qzv2')
    urls = []
    for li in li_elements:
        a_elements = li.find_all('a', href=True)
        for a in a_elements:
            href_valor = a.get('href')
            if href_valor:
                full_url = urljoin('https://www.zoopla.co.uk/', href_valor)
                if 'tel:' not in full_url and not full_url.startswith("https://www.zoopla.co.uk/find-agents/contact/"):
                    urls.append(full_url)
    return soup, urls

def fetch_data(url, all_urls, scraped_urls):
    driver_path = '/home/german/Documentos/Work'  
    options = ChromeOptions()
    driver = Chrome(executable_path=driver_path, options=options)
    try:
        driver.get(url)
        soup, new_urls = extract_data_from_page(driver)

        for url in new_urls:
            if url not in all_urls:
                scraped_urls.append(url)
                all_urls.add(url)

        # Verificar si no hay nuevas URLs en la página actual
        if not new_urls:
            # Verificar si no hay más elementos para extraer
            if not soup.find_all('li', class_='_1815qzv2'):
                return False
        return True

    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return False

    finally:
        driver.quit()


base_url = "https://www.zoopla.co.uk/find-agents/estate-agents/"
all_urls = set()
scraped_urls = []

def fetch_data(url, all_urls, scraped_urls):
    driver_path = '/home/german/Documentos/Work'  
    options = ChromeOptions()
    driver = Chrome(executable_path=driver_path, options=options)
    try:
        driver.get(url)
        soup, new_urls = extract_data_from_page(driver)

        for url in new_urls:
            if url not in all_urls:
                scraped_urls.append(url)
                all_urls.add(url)

        # Verificar si no hay nuevas URLs en la página actual
        if not new_urls:
            # Verificar si no hay más elementos para extraer
            if not soup.find_all('li', class_='_1815qzv2'):
                return False
        return True

    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return False

    finally:
        driver.quit()

for url in saranga:
    page_number = 1
    while True:
        url_to_scrape = f"{url}?pn={page_number}"
        print(f"Scrapeando página: {url_to_scrape}")  # Imprimir la página actual
        if not fetch_data(url_to_scrape, all_urls, scraped_urls):
            break
        page_number += 1
          # Espera para no sobrecargar el servidor

# Imprimir las URLs scrapeadas
for url in scraped_urls:
    print(url)

    #-----------------------------------------
    saranga1=fetch_data_pages(all_urls[:1])
    
