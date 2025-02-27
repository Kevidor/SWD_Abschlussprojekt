import streamlit as st
import os

def run():
    st.title("Home")
    columns = st.columns(2, gap="small")
    with columns[0]:
        st.header("How to create a Mechanism")
        st.markdown("If you want to configure your own mechanism, click on “Structure” at the top. There you can draw any mechanism and display a preview, which you can then animate to see the motion sequence.")
        st.markdown("""To create a mechanism, you have to go to the Structure tab, where you will find the tables on the left to configure joints etc. On the right-hand side you will see a preview of what your configuration will look like. There are different buttons, which already tell you by their name what they do.
        If the degrees of freedom are not equal to zero, the mechanism will be blocked by the animation.""")
    with columns[1]:
        st.header("import our drawing")
        st.markdown("If you have already drawn a mechanism on a sheet and you want to load it into the web interface, then click on Import, where you can save and edit your drawing according to the criteria mentioned on the page.")
        
    st.header("Warnings")
    st.markdown("""The warning explains that two identical joints were used in the link "X". 
             This means that a connection is not possible. A warning is shown below as an example:""")
    st.warning(f"⚠️ Please choose different joints for Link 1")
    st.header("Error")
    st.markdown(""" Once the, as explained in the first warning, it cannot have a connection to two identical joints, as soon as this occurs, 
                the will be disabled due to this warning. Example of this error:""")
    st.error("Please Check your Link Table")
    st.markdown("""If no joints have been created, no links can be possible, so it is pointed out that you should create a joint first. 
                Example of this error:""")
    st.error("There are not one Joints available")


