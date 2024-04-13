import streamlit as st
from fuzzywuzzy import fuzz
import requests
from bs4 import BeautifulSoup

# Database (TEMP: MOCK)
bogo_items = []

# Get Store ID
def get_store_id(zipcode):
    response = requests.get('https://accessibleweeklyad.publix.com/PublixAccessibility/StoreLocation/Index/?StoreID=2729441&CityStateZip=' + zipcode)
    soup = BeautifulSoup(response.content, 'html.parser')

    store = soup.find('div', class_='storeLocation_listRepeater')

    if store:
        store_id = store.find('a', class_='action-tracking-nav')['href'].split('=')[-1]
        print(store_id)
        return store_id
    else:
        print("No store found")
        return None

# Get BOGO Deals
def get_bogo_deals(store_id):
    response = requests.get('https://accessibleweeklyad.publix.com/PublixAccessibility/BrowseByListing/ByCategory/?&CategoryID=5232540&StoreID=' + store_id)
    soup = BeautifulSoup(response.content, 'html.parser')
    bogo_deals = soup.find_all('div', class_='unitB')

    # Get product names
    for deal in bogo_deals:
        product_name = deal.find('h2', class_='ellipsis_text').text
        bogo_items.append(product_name)

# Search for items in the shopping list
def find_items(shopping_list, bogo_items):
    matching_items = []

    for shopping_item in shopping_list:
        for bogo_item in bogo_items:
            fuzz_score = fuzz.ratio(shopping_item.lower(), bogo_item.lower())
            if fuzz_score > 45:
                matching_items.append(bogo_item)

    return list(set(matching_items))


# Page Configurations
st.set_page_config(
    page_title = 'PublixAlert',
    page_icon = '🛒'
)

st.title('🛒 PublixAlert 🛒')
st.divider()


# User Settings Page
st.subheader('User Settings')

phone_number = st.text_input('Enter Your Phone Number:')
zipcode = st.text_input('Enter Your Zipcode:')
shopping_list_input = st.text_area('Enter Your Shopping list:')


if st.button('Save'):
    store_id = get_store_id(zipcode)
    get_bogo_deals(store_id)

    shopping_list = shopping_list_input.split("\n")
    shopping_list = [item.strip() for item in shopping_list if item.strip()]
    matching_list = find_items(shopping_list, bogo_items)
    
    st.success('Settings Saved')

    st.write("Current BOGO Deals:")
    st.write(matching_list)

