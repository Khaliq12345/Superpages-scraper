import requests
from bs4 import BeautifulSoup
import pandas as pd
from latest_user_agents import get_random_user_agent
ua = get_random_user_agent()

keyword = input('Keyword: ')
location = input('Location: ')
pages = int(input('Number of pages: '))

def scrape():
    item_list = []
    x = 0
    for i in range(1, pages):
        x = x + 1
        headers = {'User-Agent': ua}
        response = requests.get(f'https://www.superpages.com/search?search_terms={keyword}&geo_location_terms={location}&page={i}', headers=headers)
        print(f'Page {x}')

        soup = BeautifulSoup(response.text, 'html.parser')
        try:
            cards = soup.select('.result')
            for card in cards:
                try:
                    name = card.select_one('.business-name').text
                except:
                    name = None
                try:
                    link = card.select_one('.weblink-button')['href']
                except:
                    link = None
                try:
                    phone = card.select_one('.phone').text.replace('Call Now', '')
                except:
                    phone = None
                try:
                    address1 = card.select_one('.street-address').text
                except:
                    address1 = None
                try:
                    super_page_link = 'https://www.superpages.com' + cards[0].select_one('.business-name')['href']
                except:
                    super_page_link = None
                try:
                    reviews = card.select_one('.count').text.replace(')', '').replace('(', '')
                except:
                    reviews = None
                items = {
                    'Name': name,
                    'Website/social': link,
                    'Phone': phone,
                    'Address 1': address1,
                    'Reviews': reviews,
                    'Super-page Link': super_page_link
                }
                item_list.append(items)
        except:
            pass

    df = pd.DataFrame(item_list)
    df.to_csv('superpages.csv')
    print(df)

scrape()