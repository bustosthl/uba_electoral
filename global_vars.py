from streamlit_javascript import st_javascript

st_theme = st_javascript("""window.getComputedStyle(window.parent.document.getElementsByClassName("stApp")[0]).getPropertyValue("color-scheme")""")
if st_theme == "light":
    color_linea = 'black'
else:
    color_linea = 'white'

#from user_agents import parse
ua_string = st_javascript("""window.navigator.userAgent;""")
if "mobile" in str(ua_string).lower():
    isMobile=True
else:
    isMobile=False