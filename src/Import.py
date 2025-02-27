import streamlit as st
import os
from mechanism import Mechanism
def run():
    
    if "read_pic" not in st.session_state:
        st.session_state.read_pic = False
    
    if "pic_name" not in st.session_state:
        st.session_state.pic_name = None
        
    st.header("Import your Picture")
    st.subheader("basic condition:")
    st.write("- The picture should be square")
    st.write("- The image must be well lighted ")
    st.write("- The joints and the links must be clearly recognizable")
    
    if st.button("Import Image"):
        meckanism = Mechanism("Import")
        meckanism.create_from_sketch(os.path.join(os.path.dirname(os.path.abspath(__file__)),"img\photo_image.jpeg"))
        st.info(meckanism)
        meckanism.store_data()
        meckanism.clear()