from streamlit_javascript import st_javascript
import streamlit as st

st_theme = st_javascript("""window.getComputedStyle(window.parent.document.getElementsByClassName("stApp")[0]).getPropertyValue("color-scheme")""")
if st_theme == "light":
    color_linea = 'black'
else:
    color_linea = 'white'

pcolor = st.get_option('theme.primaryColor')
bcolor = st.get_option('theme.backgroundColor')
sbcolor = st.get_option('theme.secondaryBackgroundColor')