import requests
from bs4 import BeautifulSoup
import json
import time

base_url = "https://www.jumia.co.ke/televisions/?display_size=55.0--55"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
}
def scrape_product_details(product_url):
    print(f"Scraping product details from {product_url}")
    
    response = requests.get(product_url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to retrieve product details. Status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    
    product_name = soup.find('h1', class_='-fs20 -pts -pbxs').text.strip() if soup.find('h1', class_='-fs20 -pts -pbxs') else "N/A"
    price = soup.find('span', class_='-b -ltr -tal -fs24').text.strip() if soup.find('span', class_='-b -ltr -tal -fs24') else "N/A"
    availability = soup.find('p', class_="-df -i-ctr -fs12 -pbs -gy5").text.strip() if soup.find('p', class_="-df -i-ctr -fs12 -pbs -gy5") else "N/A"
    rating = soup.find('div', class_="stars _m _al").text.strip() if soup.find('div', class_="stars _m _al") else "N/A"
    
    
    product_details = {
        'product_name': product_name,
        'price': price,
        'availability': availability,
        'rating': rating
    }
    return product_details

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
        link_tag = product.find('a')
        if link_tag and 'href' in link_tag.attrs:
            link = link_tag['href']
            full_link = f"https://www.jumia.co.ke{link}" 

            product_details = scrape_product_details(full_link)

            if product_details:
                product_data.append(product_details)
            
            time.sleep(2)

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

with open('jumia_televisions_55inch_detailed.json', 'w') as f:
    json.dump(product_data, f, indent=4)