import streamlit as st
import os
from time import sleep
        
def run():
    
    if "read_pic" not in st.session_state:
        st.session_state.read_pic = False
    
    if "pic_name" not in st.session_state:
        st.session_state.pic_name = None
        
    st.header("Import your Picture")
    st.subheader("basic condition:")
    st.write("- The drawing must be on a squared sheet of paper")
    st.write("- The image must be well lighted ")
    st.write("- The joints and the links must be clearly recognizable")
    
    if st.session_state.read_pic is False:
        st.session_state.pic_name = st.text_input("Enter the Picture Name:")
        if st.button("Add the Picture", disabled=True if st.session_state.pic_name == None else False  ):
            st.info("Please, wait for your picture")
            st.session_state.read_pic = True
            st.rerun()

    else:        
        cols = st.columns(2)
        if st.session_state.read_pic is True:
            for match_file in os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),"img")):
                if st.session_state.pic_name == match_file:
                    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"img",st.session_state.pic_name), "rb") as f:
                        gif_bytes = f.read()
                        st.image(gif_bytes, caption="Createeed Picture")
            with cols[0]:
                if st.button("Submit"):
                    st.success("You importet your picture")
                    st.rerun()  
            with cols[1]:
                if st.button("Retry"):
                    st.session_state.read_pic = False
                    st.rerun()
    