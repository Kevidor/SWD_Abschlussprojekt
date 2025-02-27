import pandas as pd
import streamlit as st
from mechanism_components import Joint, Link, Rotor
from mechanism import Mechanism
import matplotlib.pyplot as plt
from time import sleep
import os

def run():
    st.title("Mechanism")
    
    # Session_States
   
    if "df_joint" not in st.session_state:
        st.session_state.df_joint = pd.DataFrame([{"name":"Start","x": 10 , "y" :10, "is_fixed": True,"is_drawn": False}])
        
    if "df_link" not in st.session_state:
        st.session_state.df_link = pd.DataFrame([{"joint1": None, "joint2": None, "line_style":"-", "line_color": "black"}])
    
    if "rotor" not in st.session_state:
        st.session_state.rotor = pd.DataFrame([{"x": 25 , "y" :25,"rot_joint": 0}])
        
    if "is_correct" not in st.session_state:
        st.session_state.is_correct = True
        
    if "valid" not in st.session_state:
        st.session_state.valid = True
    
    if "rotor_valid" not in st.session_state:
        st.session_state.rotor_valid = True
        
    if "start_anim" not in st.session_state:
        st.session_state.start_anim = False
    
    if "start_config" not in st.session_state:
        st.session_state.start_config = True
        
    if "disable_sim" not in st.session_state:
        st.session_state.disable_sim = True

    if "available_projects" not in st.session_state:
        st.session_state.available_projects = Mechanism.find_all()  
    
    if "mechanism" not in st.session_state:
        st.session_state.mechanism = Mechanism(None)
    
    if "load_project" not in st.session_state:
        st.session_state.load_project = {}
     
    if "project_loaded" not in st.session_state:
        st.session_state.project_loaded = False
        
    if "selected_project" not in st.session_state:
        st.session_state.selected_project = None
        
        
    #Define columns 
    cols = st.columns(2,gap="medium",border=True)
    #Left side: Configuration of the Mechanism
    with cols[0]:
        if st.session_state.start_config:
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
                                                                #Joint
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
            st.subheader(body="Joints")
            st.markdown("Press ➕ to add a new row")
            st.markdown("Select der Joint and Press 🗑️ to delete the Joint""")
            # Add new row, if you press a button
            
            if st.session_state.df_joint.empty:
                if st.button("Add first row for joint"):
                    st.session_state.df_joint = pd.DataFrame([{"name": "fix Joint", "x": 10, "y": 10, "is_fixed": True,"is_drawn":False}])
                    st.rerun()
            else:
                edit_df_joint = st.data_editor(st.session_state.df_joint, 
                                               column_config = {
                                                "name": st.column_config.TextColumn(),
                                                "x": st.column_config.NumberColumn(min_value=-100, max_value=100),
                                                "y": st.column_config.NumberColumn(min_value=-100, max_value=100),
                                                "is_fixed": st.column_config.CheckboxColumn("is_fixed",default=False),
                                                "is_drawn": st.column_config.CheckboxColumn("is_drawn",default=False)},
                                                num_rows="dynamic",
                                                hide_index=False,
                                                use_container_width=True)	
                
                if not edit_df_joint.equals(st.session_state.df_joint):
                    st.session_state.df_joint = edit_df_joint
                    st.session_state.df_joint.reset_index(drop=True, inplace=True)
                    st.rerun()
                #Debugging
                #for index,row in st.session_state.df_joint.iterrows():
                #    st.write(f"Index: {index}, x: {row['x']}, y: {row['y']}, is_fixed: {type(row['is_fixed'])}, is_drawn: {type(row['is_drawn'])}")

            if len(st.session_state.df_joint) != 0:
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
                                                                #Rotor
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
                st.subheader("Choose your rotor")
                if st.session_state.rotor.empty:
                    if st.button("Add first row for Rotor"):
                        st.session_state.rotor = pd.DataFrame([{"x": 25 , "y" :25,"rot_joint": 0}])
                        st.rerun()
                else:
                    edit_df_rotor = st.data_editor(st.session_state.rotor,
                                                   column_config= {
                                                       "x": st.column_config.NumberColumn(min_value=-100, max_value=100),
                                                        "y": st.column_config.NumberColumn(min_value=-100, max_value=100),
                                                       "rot_joint": st.column_config.SelectboxColumn("rot_joint", options=edit_df_joint.index, default=None)},
                                                   num_rows="dynamic",
                                                   hide_index=False,
                                                   use_container_width=True)
                    if  not edit_df_rotor.equals(st.session_state.rotor):
                        st.session_state.rotor_valid = True
                        st.session_state.rotor = edit_df_rotor
                        st.session_state.rotor.reset_index(drop=True, inplace=True)
                        st.rerun()
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
                                                                #Link
#--------------------------------------------------------------------------------------------------------------------------------------------------------------               
                st.subheader("Link")
                if st.session_state.df_link.empty:
                    if st.button("add first row for link"):
                        st.session_state.df_link = pd.DataFrame([{"joint1": None, "joint2": None, "line_style":"-", "line_color": "black"}])
                        st.rerun()
                else:
                    edit_df_link = st.data_editor(st.session_state.df_link,
                                                  column_config=
                                                        {
                                                         "joint1": st.column_config.SelectboxColumn("joint1", options=edit_df_joint.index, default=None),
                                                         "joint2": st.column_config.SelectboxColumn("joint2", options=edit_df_joint.index, default= None),
                                                         "line_style": st.column_config.SelectboxColumn("line_style",options=["-","--","-."],default="-"),
                                                         "line_color": st.column_config.SelectboxColumn("line_color", options=["black","blue","red", "magenta", "green", "yellow", "purple"], default="black")},
                                                        num_rows="dynamic",
                                                        hide_index=False,
                                                        use_container_width=True)
                
                    if not edit_df_link.equals(st.session_state.df_link):
                        st.session_state.valid = True

                        for index, row in edit_df_link.iterrows():
                            if row["joint1"] is None or row["joint2"] is None:
                                    st.warning("⚠️ Missing joints!")
                                    st.session_state.valid = False
                            else:
                                if row["joint1"] == row["joint2"]:
                                    st.warning(f"⚠️ Please choose different joints for Link{index}")
                                    st.session_state.valid = False
                                    st.session_state.is_correct = False
                                else:
                                    st.session_state.is_correct = True

                        if st.session_state.is_correct:    
                            st.session_state.df_link = edit_df_link
                            st.session_state.df_link.reset_index(drop=True, inplace=True)
                            st.rerun()
                
                #for index,row in st.session_state.df_link.iterrows():
                #    st.write(f"Index: {type(index)}, Joint1: {type(row['joint1'])}, Joint2: {type(row['joint2'])}")
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
                                                                #Action_buttom
#-------------------------------------------------------------------------------------------------------------------------------------------------------------- 
                
                if st.button("Check Degrees of freedom", use_container_width=True):  
                    st.session_state.mechanism.clear()
                    for index_joint, row_joint in st.session_state.df_joint.iterrows():
                        #st.info(f"{row_joint}")
                        Joint(id=int(index_joint),name=str(row_joint["name"]), x=float(row_joint["x"]), y=float(row_joint["y"]), is_fixed=bool(row_joint["is_fixed"]),is_drawn=bool(row_joint["is_drawn"]))
                    #st.info(Joint.joints)

                    for id, row_link in  st.session_state.df_link.iterrows():
                        j1_index = row_link["joint1"]
                        j2_index = row_link["joint2"]
                        joint1, joint2  = None, None
                        for j in Joint.joints:
                            if j.id == j1_index:
                                joint1 = j
                            if j.id == j2_index:
                                joint2 = j
                        Link(int(id), joint1,joint2, str(row_link["line_style"]), str(row_link["line_color"]))
                    #st.info(Link.links)
                    
                
                    for index_rotor, row_rotor in st.session_state.rotor.iterrows():
                        rotor_joint_index = row_rotor["rot_joint"]
                        joint_rot = None 
                        for j in Joint.joints:
                            if j.id == rotor_joint_index:
                                joint_rot = j
                        if pd.isna(row_rotor["x"]) or pd.isna(row_rotor["y"]):
                            st.error("Error: x or y is NaN for Rotor")
                        else:        
                            Rotor(id=int(index_rotor),x=int(row_rotor["x"]), y=int(row_rotor["y"]), rot_joint=joint_rot)
                    #st.info(Rotor.rotors)
                    
                    st.session_state.mechanism = Mechanism("", Joint.joints, Link.links, Rotor.rotors)
                    st.info(st.session_state.mechanism.calc_DOF())
                    #st.info(st.session_state.mechanism)
                    
                    st.session_state.disable_sim = False if st.session_state.mechanism.calc_DOF() == 0 else True
                    
                    #st.info(st.session_state.disable_sim)
                
                        
                project_name = st.text_input("Enter your Project name")
                
                cols_project = st.columns(3)
                    
                with cols_project[0]:
                    if st.button("Save Konfiguration", disabled= st.session_state.disable_sim, use_container_width=True):
                            st.session_state.mechanism.id = project_name
                            st.session_state.mechanism.store_data()
                            st.success("You saved your Project")
                            sleep(2)
                            st.rerun()
               
                with cols_project[1]:
            
                    st.session_state.selected_project = st.selectbox("Select Project ID", options=[find_project.id for find_project in Mechanism.find_all()])
                    

                    if st.button("Load Project", use_container_width=True):
                        for project_data in st.session_state.available_projects:
                            if project_data.id == st.session_state.selected_project:
                                found_project = project_data
                        
                        for joint in found_project.joints:
                            joint.pop("id", None)
                        st.session_state.df_joint = pd.DataFrame(found_project.joints)
                            
                        for link in found_project.links:
                            if isinstance(link.get("joint1"), dict) and "id" in link["joint1"]:
                                link["joint1"] = link["joint1"]["id"]
                            else:
                                link["joint1"] = None  # Fehler vermeiden, wenn kein `id`-Wert existiert

                            if isinstance(link.get("joint2"), dict) and "id" in link["joint2"]:
                                link["joint2"] = link["joint2"]["id"]
                            else:
                                link["joint2"] = None

                        st.session_state.df_link = pd.DataFrame(found_project.links)

                        for rotor in found_project.rotors:
                            if isinstance(rotor.get("rot_joint"), dict) and "id" in rotor["rot_joint"]:
                                rotor["rot_joint"] = rotor["rot_joint"]["id"]
                            else:
                                rotor["rot_joint"] = None  # Falls kein Wert vorhanden ist

                        st.session_state.rotor = pd.DataFrame(found_project.rotors)

                        st.session_state.project_loaded = True
                        st.success("Project loaded successfully")
                        st.rerun()

                    
                with cols_project[2]:
                   if st.button("Delete Project", use_container_width=True): 
                       for project_data in st.session_state.available_projects:
                            if str(project_data.id) == str(st.session_state.selected_project):
                                project_data.delete()
                                st.success("successfully deleted")
                                sleep(2)
                                st.rerun()
                                 
            else:
                st.error(" 🚨 There are not one Joints available")
        
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
                ax.set_title("Mechanismus")
                ax.set_xlabel("x")
                ax.set_ylabel("y")
                ax.scatter(st.session_state.df_joint["x"],st.session_state.df_joint["y"])
                ax.scatter(st.session_state.rotor["x"],st.session_state.rotor["y"])
                
                for index_link,row in st.session_state.df_link.iterrows():
                    j1_index = row["joint1"]
                    j2_index = row["joint2"]
                    
                    if st.session_state.df_joint.empty or j1_index not in st.session_state.df_joint.index or j2_index not in st.session_state.df_joint.index or row["line_style"] is None  or row["line_color"] is None:
                        continue
                    else:
                        x_values = [st.session_state.df_joint.loc[j1_index, "x"] , st.session_state.df_joint.loc[j2_index, "x"]]
                        y_values = [st.session_state.df_joint.loc[j1_index, "y"], st.session_state.df_joint.loc[j2_index, "y"]]
                        Linestyle : str = row["line_style"]
                        color: str = row["line_color"]
                        ax.plot(x_values, y_values, Linestyle, linewidth=2, color = color)
                
                for index,row in st.session_state.df_joint.iterrows():
                    ax.text(row["x"] + 2, row["y"] + 3, row["name"], fontsize=12, color="black")
                
                for index,row in st.session_state.rotor.iterrows():
                    if not st.session_state.df_joint.empty:
                        joint_rot_plt = row["rot_joint"]
                        
                        if pd.isnull(row["x"]) or pd.isnull(row["y"]) or pd.isnull(joint_rot_plt):
                            continue
                        else:
                            if joint_rot_plt in st.session_state.df_joint.index:
                                x_values = [row["x"], st.session_state.df_joint.loc[joint_rot_plt, "x"]]
                                y_values = [row["y"], st.session_state.df_joint.loc[joint_rot_plt, "y"]]
                                ax.plot(x_values,y_values,"--", color = "orange")
                            else:
                                st.error("🚨 No joint available")
                ax.grid()
                st.pyplot(fig)
                
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
                                                                #Action_buttom
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
                cols = st.columns(2)
                with cols[0]:
                    if st.button("Start Animation", disabled= st.session_state.disable_sim):
                        st.session_state.start_anim = True
                        st.session_state.start_config = False
                        st.rerun()
                        
                with cols[1]:
                    fig.savefig("Preview_Mechanimus.png", transparent=None, dpi= 'figure')
                    with open("Preview_Mechanimus.png", "rb") as preview:
                        st.download_button(label="Save Preview-Ilustration",data= preview, file_name="Preview_Mechanimus.png", mime="image/png")
            else:
                st.info("The animation could take a few seconds!")
                st.session_state.mechanism.create_animation()
                
                with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "mechanismus_animation.gif"), "rb") as f:
                    gif_bytes = f.read()
                    st.image(gif_bytes, caption="Mechanism-Animation", use_container_width=True)
                
                columns_button = st.columns(3,gap="small")
                
                with columns_button[0]:
                    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "mechanismus_animation.gif"), "rb") as f:
                        gif_bytes = f.read()
                        st.download_button(label="Download GIF", data=gif_bytes, file_name="mechanism_animation.gif", mime="image/gif", use_container_width=True)
                
                with columns_button[1]:
                    if st.button("Stop Animation", use_container_width=True):
                        st.success("You stopped your Animation")
                        st.session_state.start_config = True
                        st.session_state.start_anim = False
                        st.rerun()
                
                with columns_button[2]:
                    if not st.session_state.disable_sim:
                        cvs_file = st.session_state.mechanism.create_csv()
                        st.download_button(label="Download CSV", data=cvs_file, file_name="mechanism_Data.csv", mime="text/.csv", use_container_width=True)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
                                                                #Error
#--------------------------------------------------------------------------------------------------------------------------------------------------------------      
        else:
                st.error("🚨 Please Check your Link Table")