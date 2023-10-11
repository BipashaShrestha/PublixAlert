import streamlit as st
from fuzzywuzzy import fuzz

mock_bogo_items = ["Skinless Chicken wings", "Annie's Organic Fruit Snacks", "Ball Park Franks", "Barilla Pasta", "Fresh Mozzarella Cheese", "Ice cream", "Milano Cookies", "Fiji water"]

# Functions
def find_items(shoppling_list, bogo_items):
    matching_items = []

    for shopping_item in shopping_list:
        for bogo_item in bogo_items:
            fuzz_score = fuzz.ratio(shopping_item.lower(), bogo_item.lower())
            if fuzz_score > 30:
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
    matching_list = find_items(shopping_list, mock_bogo_items)
    
    st.success('Settings Saved')

    st.write("Current BOGO Deals:")
    st.write(matching_list)

