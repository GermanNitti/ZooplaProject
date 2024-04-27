from undetected_chromedriver import Chrome, ChromeOptions
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin

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

base_url = "https://www.zoopla.co.uk/find-agents/estate-agents/slough/?pn="
all_urls = set()
scraped_urls = []

page_number = 1
while True:
    url_to_scrape = base_url + str(page_number)
    print(f"Scrapeando página: {url_to_scrape}")  # Imprimir la página actual
    if not fetch_data(url_to_scrape, all_urls, scraped_urls):
        break
    page_number += 1
    time.sleep(3)  # Espera para no sobrecargar el servidor

# Imprimir las URLs scrapeadas
for url in scraped_urls:
    print(url)
