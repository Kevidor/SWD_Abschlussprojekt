import pandas as pd
import streamlit as st
from mechanism_components import Joint, Link, Rotor
from mechanism import Mechanism
import matplotlib.pyplot as plt
from time import sleep
import os
def run():
    st.title("Mechanism")
    mechanism = Mechanism(None)
    
    # Session_States
   
    if "df_joint" not in st.session_state:
        st.session_state.df_joint = pd.DataFrame([{"Name":"Start","x": 10 , "y" :10, "is_fixed": True,"is_drawn": False}])
        
    if "df_link" not in st.session_state:
        st.session_state.df_link = pd.DataFrame([{"joint1": None, "joint2": None, "Linestyle":"-", "Line_color": "black"}])
    
    if "rotor" not in st.session_state:
        st.session_state.rotor = pd.DataFrame([{"x": 25 , "y" :25,"joint": 0}])
        
    if "is_correct" not in st.session_state:
        st.session_state.is_correct = True
        
    if "valid" not in st.session_state:
        st.session_state.valid = True
    
    if "rotor_valid" not in st.session_state:
        st.session_state.rotor_valid = True
        
    if "start_anim" not in st.session_state:
        st.session_state.start_anim = False
    
    if "gif" not in st.session_state:
        st.session_state.gif =None
    
    if "start_config" not in st.session_state:
        st.session_state.start_config = True
        
    if "disable_sim" not in st.session_state:
        st.session_state.disable_sim = True

    #Define columns    
    cols = st.columns(2,gap="medium",border=True)
    #Left side: Configuration of the Mechanism
    with cols[0]:
        #col_borders = st.columns(2,gap="small")
        #st.subheader("Draw Settings")
        #with col_borders[0]:
        #    st.write("Minimum Values:")
        #    min_x = st.text_input("min. x = ", value=0)
        #    min_y = st.text_input("min. y = ", value=0)
        #    st.rerun()
        #    
        #with col_borders[1]:
        #    st.write("Maximum Values:")
        #    max_x = st.text_input("max. x = ",value=50)
        #    max_y = st.text_input("max. y = ",value=55)
        #    st.rerun()
        if st.session_state.start_config:
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
                                                                #Joint
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
            st.subheader("Joints")
            st.markdown("Press ➕ to add a new row")
            st.markdown("Select der Joint and Press 🗑️ to delete the Joint""")
            # Add new row, if you press a button
            if st.session_state.df_joint.empty:
                if st.button("Add first row for joint"):
                    st.session_state.df_joint = pd.DataFrame([{"Name": "fix Joint", "x": 10, "y": 10, "is_fixed": True,"is_drawn":False}])
                    st.rerun()
                    
            else:
                edit_df_joint = st.data_editor(st.session_state.df_joint, 
                                               column_config = {
                                                "Name": st.column_config.TextColumn(),
                                                "x": st.column_config.NumberColumn(min_value=-100, max_value=100),
                                                "y": st.column_config.NumberColumn(min_value=-100, max_value=100),
                                                "is_fixed": st.column_config.CheckboxColumn("is_fixed",default=False),
                                                "is_drawn": st.column_config.CheckboxColumn("is_drawn",default=False)},
                                                num_rows="dynamic",
                                                hide_index=False,
                                                use_container_width=True)	
                
                if not edit_df_joint.equals(st.session_state.df_joint):
                    df_joint_update = edit_df_joint.copy()
                    st.session_state.df_joint = df_joint_update
                    st.session_state.df_joint.reset_index(drop=True, inplace=True)
                    st.rerun()
                    
                #Debugging
                for index,row in st.session_state.df_joint.iterrows():
                    st.write(f"Index: {index}, x: {row['x']}, y: {row['y']}, is_fixed: {type(row['is_fixed'])}, is_drawn: {type(row['is_drawn'])}")
 
            if len(st.session_state.df_joint) != 0:
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
                                                                #Rotor
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
                st.subheader("Choose your rotor")
                if st.session_state.rotor.empty:
                    if st.button("Add first row for Rotor"):
                        st.session_state.rotor = pd.DataFrame([{"x": 25 , "y" :25,"joint": 0}])
                        st.rerun()
                else:
                    edit_df_rotor = st.data_editor(st.session_state.rotor,
                                                   column_config= {
                                                       "x": st.column_config.NumberColumn(),
                                                        "y": st.column_config.NumberColumn(),
                                                       "joint": st.column_config.SelectboxColumn("joint", options=edit_df_joint.index, default=None)},
                                                   num_rows="dynamic",
                                                   hide_index=False,
                                                   use_container_width=True)
                
                
                    if  not edit_df_rotor.equals(st.session_state.rotor):
                        st.session_state.rotor_valid = True    
                        df_rotor_update = edit_df_rotor.copy()
                        st.session_state.rotor = df_rotor_update
                        st.session_state.rotor.reset_index(drop=True, inplace=True)
                        st.rerun()
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
                                                                #Link
#--------------------------------------------------------------------------------------------------------------------------------------------------------------               
                st.subheader("Link")
                if not st.session_state.df_link.empty:
                    edit_df_link = st.data_editor(st.session_state.df_link,
                                                  column_config=
                                                        {
                                                         "joint1": st.column_config.SelectboxColumn("joint1", options=edit_df_joint.index, default= None),
                                                         "joint2": st.column_config.SelectboxColumn("joint2", options=edit_df_joint.index, default = None),
                                                         "Linestyle": st.column_config.SelectboxColumn("Linestyle",options=["-","--","-."],default="-"),
                                                         "Line_color": st.column_config.SelectboxColumn("Line_color", options=["black","blue","red", "magenta", "green", "yellow", "purple"], default="black")},
                                                        num_rows="dynamic",
                                                        hide_index=False,
                                                        use_container_width=True)
                    if not edit_df_link.equals(st.session_state.df_link):
                        st.session_state.valid = True
                        for index, row in edit_df_link.iterrows():
                            if row["joint1"] is None or row["joint2"] is None:
                                continue
                            else:
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
                
                else:
                    if st.button("add first row for link"):
                        st.session_state.df_link = pd.DataFrame([{"joint1": None, "joint2": None, "Linestyle":"-", "Line_color": "black"}])
                        st.rerun()
                        
                for index,row in st.session_state.df_link.iterrows():
                    st.write(f"Index: {type(index)}, Joint1: {type(row['joint1'])}, Joint2: {type(row['joint2'])}")
                
                if st.button("Check Degrees of freedom"):  
                    mechanism.clear()
                    for index_joint, row_joint in st.session_state.df_joint.iterrows():
                        Joint(index_joint,
                              row_joint["Name"], 
                              row_joint["x"], 
                              row_joint["y"], 
                              row_joint["is_fixed"],
                              is_drawn=row_joint["is_drawn"])
                        
                    for index_link, row_link in  st.session_state.df_link.iterrows():
                        j1_index = row_link["joint1"]
                        j2_index = row_link["joint2"]
                        joint1, joint2  = None, None
                        
                        for j in Joint.joints:
                            if j.index == j1_index:
                                joint1 = j
                            if j.index == j2_index:
                                joint2 = j
                        Link(index_link, joint1,joint2, row_link["Linestyle"], row_link["Line_color"])
                        
                    for index_rotor, row_rotor in st.session_state.rotor.iterrows():
                        rotor_joint_index = row_rotor["joint"]
                        joint_rot = None 
                        
                        for j in Joint.joints:
                            if j.index == rotor_joint_index:
                                joint_rot = j
                        Rotor(x=row_rotor["x"], y=row_rotor["y"], rot_joint=joint_rot)
                    st.info(mechanism.calc_DOF())
                    st.session_state.disable_sim = False if mechanism.calc_DOF() == 0 else True
                    st.info(st.session_state.disable_sim)
                name_project = st.text_input("Name of the Konfiguration:")

                if st.button("Save Konfiguration", disabled= True if name_project == None else False):
                    Project = Mechanism(name_project)
                    Project.store_data()
                    
                    
            else:
                st.error("There are not one Joints available")
            #st.write("- Arrow-right solid line")
            #st.write("- - Arrow-right dahsed line")
            #st.write("-. Arrow-right dash dot line")
        else:
            st.info("Stop your animation to do a configuration")
            
               
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
                                                                #Graphics
#--------------------------------------------------------------------------------------------------------------------------------------------------------------      
               
    with cols[1]:
        st.subheader("Preview")
        if st.session_state.valid:
            if st.session_state.start_anim == False:                  
            #for a Preview, before starting an animation
            
                fig, ax = plt.subplots()    
                ax.set_xlim(-100,100)
                ax.set_ylim(-100,100)
                ax.scatter(st.session_state.df_joint["x"],st.session_state.df_joint["y"])
                ax.scatter(st.session_state.rotor["x"],st.session_state.rotor["y"])
                
                for index,row in st.session_state.df_link.iterrows():
                    j1_index = row["joint1"]
                    j2_index = row["joint2"]
                    if not st.session_state.df_joint.empty:
                        if (j1_index is None and j2_index is None) or row["Linestyle"] is None  or row["Line_color"] is None:
                            continue
                        else:   
                            x_values = [st.session_state.df_joint.loc[j1_index, "x"] , st.session_state.df_joint.loc[j2_index, "x"]]
                            y_values = [st.session_state.df_joint.loc[j1_index, "y"], st.session_state.df_joint.loc[j2_index, "y"]]
                            Linestyle : str = row["Linestyle"]
                            color: str = row["Line_color"]
                            ax.plot(x_values, y_values, Linestyle, linewidth=2, color = color)
                
                for index,row in st.session_state.df_joint.iterrows():
                    ax.text(row["x"] + 2, row["y"] + 3, row["Name"], fontsize=12, color="black")
               
                for index,row in st.session_state.rotor.iterrows():
                    if not st.session_state.df_joint.empty:
                        joint_rot_plt = row["joint"]
                        if row["x"] is None or row["y"] is None or joint_rot_plt is None:
                            continue
                        else:
                            x_values = [row["x"] , st.session_state.df_joint.loc[joint_rot_plt, "x"]]
                            y_values = [row["y"], st.session_state.df_joint.loc[joint_rot_plt, "y"]]
                            ax.plot(x_values,y_values,"--", color = "orange")
                ax.grid()
                st.pyplot(fig)
                #st.info(mechanism.rotors)
                #st.info(mechanism.links)
                #st.info(mechanism.joints)
                cols = st.columns(3)
                with cols[0]:
                    if st.button("Start Animation", disabled= st.session_state.disable_sim):
                        st.session_state.start_anim = True
                        st.session_state.start_config = False
                        st.rerun()
               
                with cols[1]:
                    if not st.session_state.disable_sim:
                        st.session_state.gif = os.path.join(os.path.curdir)
                        cvs_file = mechanism.create_csv()
                        st.download_button(label="Download CSV", data=cvs_file, file_name="mechanism_Data.csv", mime="text/.csv")
                
                with cols[2]:
                    file =fig.savefig("Preview_Mechanimus.png", transparent=None, dpi= 'figure')
                    with open("Preview_Mechanimus.png", "rb") as preview:
                        st.download_button(label="Save Preview-Ilustration",data= preview, file_name="Preview_Mechanimus.png", mime="image/png")
            else:
                st.info("The animation could take a few seconds!")
                mechanism.create_animation()
                with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "mechanismus_animation.gif"), "rb") as f:
                    gif_bytes = f.read()
                    st.image(gif_bytes, caption="Mechanism-Animation", use_container_width=True)
                
                columns_button = st.columns(3,gap="small")
                with columns_button[0]:
                    st.download_button(label="Download GIF", data=st.session_state.gif, file_name="mechanism_animation.gif", mime="image/gif")
                with columns_button[1]:
                    if st.button("Stop Animation"):
                        st.success("You stopped your Animation")
                        st.session_state.start_config = True
                        st.session_state.start_anim = False
                        st.rerun()
                
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
                                                                #Error
#--------------------------------------------------------------------------------------------------------------------------------------------------------------      
        else:
                st.error("Joint conflict")
            