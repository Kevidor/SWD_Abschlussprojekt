import pandas as pd
import streamlit as st
from mechanism_components import Joint, Link
from database_Joint import Joint_db
from database_link import Link_db 
from mechanism import Mechanism
import matplotlib.pyplot as plt
from time import sleep

def run():
    st.title("Mechanism")
    mechanism = Mechanism()
    # Session_States
    
    if "df_joint" not in st.session_state:
        st.session_state.df_joint = pd.DataFrame([{"Name":"Start","x": 25 , "y" :25, "static": True}])
        
    if "df_link" not in st.session_state:
        st.session_state.df_link = pd.DataFrame([{"joint1": None, "joint2": None, "Linestyle":"-", "Line_color": "black"}])
        
    if "is_correct" not in st.session_state:
        st.session_state.is_correct = True
        
    if "valid" not in st.session_state:
        st.session_state.valid = True
        
    if "degrees_of_freedom" not in st.session_state:
        st.session_state.degrees_of_freedom = 3
        
    if "static" not in st.session_state:
        st.session_state.static = 1
    
    if "start_config" not in st.session_state:
        st.session_state.start_config = True
    
    #Define columns    
    cols = st.columns(2,gap="medium",border=True, vertical_alignment="center")
    
    #Left side: Configuration of the Mechanism
    with cols[0]:     
            if st.session_state.start_config:
                st.subheader("Joints")
                st.markdown("Press ➕ to add a new row")
                st.markdown("Select der Joint and Press 🗑️ to delete the Joint""")

                # Add new row, if you press a button
                if st.session_state.df_joint.empty:
                     if st.button("Add first row for joint"):
                        st.session_state.df_joint = pd.DataFrame([{"Name": "fix Joint", "x": 25, "y": 25, "static": True}])
                        st.rerun()
                        
                else:
                    edit_df_joint = st.data_editor(st.session_state.df_joint, 
                                                   column_config = {
                                                    "Name": st.column_config.TextColumn(),
                                                    "x": st.column_config.NumberColumn(min_value=0, max_value=100),
                                                    "y": st.column_config.NumberColumn(min_value=0, max_value=100),
                                                    "static": st.column_config.CheckboxColumn("static",default=False)},
                                                    num_rows="dynamic",
                                                    disabled=["static"],
                                                    hide_index=False,
                                                    use_container_width=True)	

                    if not edit_df_joint.equals(st.session_state.df_joint):
                        df_joint_update = edit_df_joint.copy()
                        st.session_state.df_joint = df_joint_update
                        st.session_state.df_joint.reset_index(drop=True, inplace=True)
                        st.rerun()

                    #Debugging
                    for index,row in st.session_state.df_joint.iterrows():
                        st.write(f"Index: {index}, x: {row['x']}, y: {row['y']}, static: {row['static']}")
                    joint_dict = st.session_state.df_joint.to_dict(orient="index")
                        

                st.subheader("Link")
                
                if len(st.session_state.df_joint) != 0:
                    if not st.session_state.df_link.empty:
                        edit_df_link = st.data_editor(st.session_state.df_link,
                                                      column_config=
                                                            {
                                                             "joint1": st.column_config.SelectboxColumn("joint1", options=edit_df_joint.index),
                                                             "joint2": st.column_config.SelectboxColumn("joint2", options=edit_df_joint.index),
                                                             "Linestyle": st.column_config.SelectboxColumn("Linestyle",options=["-","--","-."]),
                                                             "Line_color": st.column_config.SelectboxColumn("Line_color", 
                                                                                                            options=["blue","red", "magenta", "green", "yellow", "purple"])},
                                                            num_rows="dynamic",
                                                            hide_index=False,
                                                            use_container_width=True)

                        if not edit_df_link.equals(st.session_state.df_link):
                            st.session_state.valid = True
                            for index, row in edit_df_link.iterrows():
                                if row["joint1"] == row["joint2"]:
                                    st.warning(f"⚠️ Please choose different joints for Link{index}")
                                    st.session_state.valid = False
                                    st.session_state.is_correct = False

                                else:
                                    st.session_state.is_correct = True

                            if st.session_state.is_correct:    
                                st.session_state.df_link = edit_df_link.copy()
                                st.session_state.df_link.reset_index(drop=True, inplace=True)
                                st.rerun()
                        
                        link_dict = st.session_state.df_link.to_dict(orient="index")
                    elif st.session_state.df_link.empty:
                        if st.button("add first row for link"):
                            st.session_state.df_link = pd.DataFrame([{"joint1": 0, "joint2": 0, "Linestyle":"-", "Line_color": "black"}])
                            st.rerun()

                    name_project = st.text_input("Name of the Konfiguration:")
                    [joint_dict,link_dict]
                    if st.button("Save Konfiguration"):
                        for (index_joint, row_joint), (index_link, row_link) in zip(st.session_state.df_joint.iterrows(), st.session_state.df_link.iterrows()):
                            #Joint(index_joint,row_joint["Name"],row_joint["x"], row_joint["y"], row_joint["static"])
                            Joint_db(index_joint,row_joint["Name"],row_joint["x"], row_joint["y"], row_joint["static"]).store_data()
                            #Link(row_link["joint1"], row_link["joint2"])
                            Link_db(index_link,row_link["joint1"], row_link["joint2"],row_link["Linestyle"],row_link["Line_color"]).store_data()
                            
                    #Debugging
                    for index,row in st.session_state.df_link.iterrows():
                        st.write(f"Index: {type(index)}, Joint1: {type(row['joint1'])}, Joint2: {type(row['joint2'])}")
                else:
                    st.error("There are not one Joints available")
                #st.write("- Arrow-right solid line")
                #st.write("- - Arrow-right dahsed line")
                #st.write("-. Arrow-right dash dot line")
            
            else:
                st.success("You started an animation")
                st.write("Stop your animation to do a configuration")      
    
    with cols[1]:
            st.subheader("Preview")
            if st.session_state.valid:
                
                #for a Preview, before starting an animation
                fig, ax = plt.subplots()
                
                ax.set_xlim(0, 100)
                ax.set_ylim(0, 100)
                ax.scatter(st.session_state.df_joint["x"],st.session_state.df_joint["y"])
                
                for index,row in st.session_state.df_link.iterrows():
                    j1_index = row["joint1"]
                    j2_index = row["joint2"]
                    if not st.session_state.df_joint.empty:
                        if j1_index != None and pd.isnull(j2_index) or j2_index != None and pd.isnull(j1_index) or pd.isnull(j1_index) and pd.isnull(j2_index) or row["Linestyle"] == None  or row["Line_color"]== None:
                            continue
                        else:    
                            x_values = [st.session_state.df_joint.loc[j1_index, "x"], st.session_state.df_joint.loc[j2_index, "x"]]
                            y_values = [st.session_state.df_joint.loc[j1_index, "y"], st.session_state.df_joint.loc[j2_index, "y"]]
                            Linestyle : str = row["Linestyle"]
                            color: str = row["Line_color"]
                    
                        ax.plot(x_values, y_values, Linestyle, linewidth=2, color = color)
                        
                for index, row in st.session_state.df_joint.iterrows():
                    ax.text(row["x"] + 1, row["y"] + 1, row["Name"], fontsize=12, color="blue")
                    
                ax.grid()
                st.pyplot(fig)
                
                cols_button = st.columns(2,gap="medium")
                with cols_button[0]:
                    if st.button("Animation"):
                        st.success("Animation started")
                        st.session_state.start_config = False    
                        sleep(2)
                        st.rerun()
                with cols_button[1]:    
                    if st.button("Stop Animation"):
                        st.success("You stopped your Animation")
                        st.session_state.start_config = True
                        sleep(2)
                        st.rerun()

            else:
                #get error caused by a joint conflict
                st.error("Joint conflict")