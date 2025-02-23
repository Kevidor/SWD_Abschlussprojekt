import streamlit as st
import pandas as pd
from time import sleep

def run():	
    st.title("Export your data")
    st.write("Export your data to a CSV file")
    select_action = st.radio("Choose your fomart to export your data:",options=["CSV","Json"])
    df = pd.DataFrame({
            "A": [1,2,3,4],
            "B": [5,6,7,8]})
    if select_action == "CSV":
        data_name = st.text_input("Put the name of your file (must end with .csv):")
        st.write("Export your data to a CSV file")
        st.write(df)
        st.write("Press the button below to export the data to a CSV file")
        if st.button("Export data"):
            if data_name != "":
                data_name = data_name+".csv"
                with open( file=data_name,mode="w",encoding= "UTF-8") as file:
                    df.to_csv(file,sep=",", index=False, header=True)
                    st.success("A CSV-File created successfully")
                    sleep(2)
                    st.rerun()
            else:
                st.error("No data name given")
    if select_action == "Json":
        st.write(df)
        st.write("Press the button below to export the data to a Json file")
        data_name = st.text_input("Put the name of your file (must end with .json):")
        if st.button("Export to json-data"):    
            if data_name != "":
                st.write("Exporting data...") 
                data_name= data_name+".json"
                with open(data_name,"w",encoding="UTF-8") as file:          
                    df.to_json(data_name,orient="columns",indent=4)
                    st.success("A Json-File created successfully")
                    sleep(2)
                    st.rerun()
            else:
                st.error("No data name given")