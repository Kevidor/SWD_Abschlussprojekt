import streamlit as st
import os
from time import sleep
import cv2
from mechanism import Mechanism

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
    


    meckanism = Mechanism()
    #meckanism.create_from_sketch( os.path.join(os.path.dirname(os.path.abspath(__file__)),"img","photo_image.jpeg"))
    meckanism.image_recognizer.load_img(os.path.join(os.path.dirname(os.path.abspath(__file__)),"img","photo_image.jpeg"))
    meckanism.image_recognizer.show_image(meckanism.image_recognizer.img)
                