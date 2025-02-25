import streamlit as st
from streamlit_option_menu import option_menu
import importlib

st.set_page_config(page_title="Mainhub",layout="wide")
selected_option = option_menu(
                              menu_title= None,
                              options=["home","Struktur"],
                              icons =["house","tools","cloud-plus"],
                              menu_icon="cast",
                              default_index=0,
                              orientation="horizontal",
                              styles={
                                    "container": {"padding": "0!important", "background-color": "#fafafa"},
                                     "icon": {"color": "green", "font-size": "25px"}, 
                                    "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "color": "black"},
                                     "nav-link-selected": {"background-color": "blue", "color": "white"},
                                    }
                            )

if selected_option == "home":
    selected_module = importlib.import_module(selected_option)
    selected_module.run()
    
if selected_option == "Struktur":
    selected_module = importlib.import_module(selected_option)
    selected_module.run()
