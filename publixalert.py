import streamlit as st
from fuzzywuzzy import fuzz
import requests
from bs4 import BeautifulSoup

bogo_items = []

response = requests.get('https://accessibleweeklyad.publix.com/PublixAccessibility/BrowseByListing/ByCategory/?ListingSort=8&StoreID=2729441&CategoryID=5232540')
soup = BeautifulSoup(response.content, 'html.parser')
bogo_deals = soup.find_all('div', class_='unitB')

for deal in bogo_deals:
    product_name = deal.find('h2', class_='ellipsis_text').text
    bogo_items.append(product_name)


# Functions
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

phone_number = st.text_input('Enter your phone number:')
local_store = st.text_input('Enter the address for your local Publix:')

shopping_list_input = st.text_area('Enter your Shopping list:')


if st.button('Save'):
    shopping_list = shopping_list_input.split("\n")
    shopping_list = [item.strip() for item in shopping_list if item.strip()]
    matching_list = find_items(shopping_list, bogo_items)
    
    st.success('Settings Saved')

    st.write("Current BOGO Deals:")
    st.write(matching_list)

