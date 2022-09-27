import streamlit as st
import importlib
# import pages    # default library name for apps
from pages import pagesContents

message = """
        __Select an application from the list below__
        """

st.set_page_config(layout = "wide") # optional

st.header("National Statistics")


# Global arrays for holding the app names, modules and descriptions of the apps
pageNames = pagesContents.pages()
descriptions = []
modules = []

# Find the apps and import them
for pagename in pageNames:
    m = importlib.import_module('.' + pagename, 'pages')
    modules.append(m)
    # If the module has a description attribute use that in the select box
    # otherwise use the module name
    try:
        descriptions.append(m.description)
    except:
        descriptions.append(pagename)

# Define a function to display the app
# descriptions instead of the module names
# in the selctbox, below
def format_func(name):
    return descriptions[pageNames.index(name)]


# Display the sidebar with a menu of apps
with st.sidebar:
    st.markdown(message)
    page = st.selectbox('Select:', pageNames, format_func=format_func)

# Run the chosen app
modules[pageNames.index(page)].run()

#st.write(f"Modules: {modules}")
#st.write(f"Module Names: {moduleNames}")
#st.write(f"Description: {descriptions}")