import os
import pandas as pd
import streamlit as st
from PIL import Image
from mechanism_components import Joint, Link
from mechanism import Mechanism
import matplotlib.pyplot as plt

def run():
    st.title("Mechanism")
    mechanism = Mechanism()
    if "df_joint" not in st.session_state:
        st.session_state.df_joint = pd.DataFrame([{"Joints":0,"x": 0 , "y" :0, "is_fixed": False}])

    if "df_link" not in st.session_state:
        st.session_state.df_link = pd.DataFrame([{"Link":0,"joint1": "None", "joint2": "None"}])

    cols = st.columns(2,gap="medium",border=True, vertical_alignment="center")
    with cols[0]:
            st.subheader("Joints")
            st.markdown("Press ➕ to add a new row")
            st.markdown("Select der Joint and Press 🗑️ to delete the Joint""")
            edit_df_joint = st.data_editor(st.session_state.df_joint, 
                                           column_config = {
                                            "Joints": st.column_config.NumberColumn("Joints",min_value=0,step=1),
                                            "x": st.column_config.NumberColumn(min_value=0, max_value=100, step=1),
                                            "y": st.column_config.NumberColumn(min_value=0, max_value=100, step=1),
                                            "is_fixed": st.column_config.CheckboxColumn("is_fixed")},
                                            num_rows="dynamic",
                                            disabled=["is_fixed"],
                                            hide_index=True,
                                            use_container_width=True)	

            #if len(edit_df_joint) > len(st.session_state.df_joint):
            #    new_row = edist_df_joint.iloc[-1]  
            #    mechanism.add_joint(new_row)
            if not edit_df_joint.equals(st.session_state.df_joint):
                st.session_state.df_joint = edit_df_joint

            st.subheader("Link")
            edit_df_link = st.data_editor(st.session_state.df_link,
                                          column_config=
                                                {
                                                 "joint1": st.column_config.SelectboxColumn("joint1", options=edit_df_joint.index),
                                                 "joint2": st.column_config.SelectboxColumn("joint2", options=edit_df_joint.index)},
                                                num_rows="dynamic",
                                                hide_index=True,
                                                use_container_width=True)

            if len(edit_df_link) > len(st.session_state.df_link):
                new_row = edit_df_link.iloc[-1]  
                if new_row["joint1"] != "None" and new_row["joint2"] != "None" and new_row["joint1"] != new_row["joint2"]:
                    mechanism.add_link(new_row)
                else:
                    st.warning("⚠️Please select two different joints")

            if not edit_df_link.equals(st.session_state.df_link):
                st.session_state.df_link = edit_df_link


    with cols[1]:
            st.subheader("Preview")
            fig, ax = plt.subplots()
            ax.set_xlim(0, 100)
            ax.set_ylim(0, 100)
            ax.plot(st.session_state.df_joint["x"], st.session_state.df_joint["y"], "ro")
            ax.grid()
            st.pyplot(fig)

            if st.button("Animation"):
                st.success("Animation started")