import requests
from bs4 import BeautifulSoup
import json

base_url = "https://www.jumia.co.ke/televisions/?display_size=55.0--55"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
}
def scrape_page(url):
    print(f"Scraping {url}")
    
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None, []

    soup = BeautifulSoup(response.content, 'html.parser')
    
    products = soup.find_all('article', class_='prd _fb col c-prd')

    product_data = []

    for product in products:
        title = product.find('h3', class_='name').text.strip()
        price = product.find('div', class_='prc').text.strip()

        link_tag = product.find('a')
        if link_tag and 'href' in link_tag.attrs:
            link = link_tag['href']
            full_link = f"https://www.jumia.co.ke{link}"
        else:
            full_link = "Link not available"

        product_info = {
            'title': title,
            'price': price,
            'link': full_link
        }

        product_data.append(product_info)

    next_page_tag = soup.find('a', {'aria-label': 'Next Page'})
    next_page_url = None
    if next_page_tag and 'href' in next_page_tag.attrs:
        next_page_url = f"https://www.jumia.co.ke{next_page_tag['href']}"

    return next_page_url, product_data

def scrape_all_pages(start_url):
    all_products = []
    next_page_url = start_url

    while next_page_url:
        next_page_url, products = scrape_page(next_page_url)
        all_products.extend(products) 

    return all_products

product_data = scrape_all_pages(base_url)

print(json.dumps(product_data, indent=4))

with open('jumia_televisions_55inch_paginated.json', 'w') as f:
    json.dump(product_data, f, indent=4)
