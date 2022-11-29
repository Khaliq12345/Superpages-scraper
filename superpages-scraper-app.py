import streamlit as st
import requests
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep
from latest_user_agents import get_random_user_agent
ua = get_random_user_agent()

st.set_page_config(page_title= 'Superpages.com Scraper', page_icon=":man:")
hide_menu = """
<style>
#MainMenu {
    visibility:hidden;}
footer {
    visibility:hidden;}
</style>
"""

def scraper1():
    item_list = []
    url = listing_url
    isNext = True
    x = 0
    col1, col2 = st.columns(2)
    progress = col1.metric('Pages scraped', 0)
    while isNext:
        x = x + 1
        headers = {'User-Agent': ua}
        response = requests.get(url, headers=headers)
        progress.metric('Pages scraped', x)
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
        try:
            n_page = soup.select_one('.next.ajax-page')['href']
            url = 'https://www.superpages.com' + n_page
        except:
            isNext = False
            break

    df = pd.DataFrame(item_list)
    col2.metric('Total data scrape', len(df))
    st.dataframe(df)

    csv = df.to_csv().encode('utf-8')
    st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='superpages-data.csv',
    mime='text/csv',
    )

def scraper2():
    item_list = []
    y = 0
    col1, col2 = st.columns(2)
    progress = col1.metric('Pages scraped', 0)
    for i in range(1, int(pages)):
        y = y + 1
        headers = {'User-Agent': ua}
        response = requests.get(f'https://www.superpages.com/search?search_terms={keyword}&geo_location_terms={location}&page={i}' ,headers=headers)
        progress.metric('Pages scraped', y)
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
    col2.metric('Total data scrape', len(df))
    st.dataframe(df)

    csv = df.to_csv().encode('utf-8')
    st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='superpages-data.csv',
    mime='text/csv',
    )

if __name__ == '__main__':
    st.title('SUPERPAGES.COM SCRAPER 🎈')
    st.markdown(hide_menu, unsafe_allow_html=True)
    st.caption('Fields to be scraped are: Name, Website, Phone, Address, Reviews, Profile link')
    tab1, tab2 = st.tabs(['Scraping with url ❄️', 'Scraping with parameters 🎉'])

    with tab1.form('Scraper with listing url'):
        listing_url = st.text_input('Paste a listing url')
        start1 = st.form_submit_button('Scrape!')
    if start1:
        scraper1()
        st.balloons()
        st.success('Done!')

    with tab2.form('Scraper with parameters'):
        keyword = st.text_input('Keyword EX: Restaurants')
        location = st.text_input('Location EX: Miami, Florida')
        pages = st.number_input('Number of pages to scrape')
        start2 = st.form_submit_button('Scrape!')
    if start2:
        scraper2()
        st.balloons()
        st.success('Done!')

