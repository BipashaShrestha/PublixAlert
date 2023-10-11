import streamlit as st


st.set_page_config(
    page_title = 'PublixAlert',
    page_icon = '🛒'
)
st.title('🛒 PublixAlert 🛒')
st.divider()

st.subheader('User Settings')

phone_number = st.text_input('Enter your phone number:')
local_store = st.text_input('Enter the address for your local Publix:')
shopping_list = st.text_area('Enter your Shopping list:')

if st.button('Save'):
    st.success('Settings Saved')

