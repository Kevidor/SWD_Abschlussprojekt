import streamlit as st
import pandas as pd
from time import sleep
def run():
    
    st.title("Import your data")
    st.write("Import your data from a CSV-File or from Json-File")

    select_action = st.radio("Choose your fomart to export your data:",options=["CSV","Json"])
    
    if select_action == "CSV":
        data_name = st.text_input("Put the name of your file:")
        if not data_name.endswith(".csv"):
            data_name += ".csv"
        st.write("Import your data to a CSV file")
        st.write("Press the button below to import the data to a CSV file")
        if st.button("IMport data"):
            try:
                if data_name != "":
                    st.write("Importing data...")
                    with open(data_name,"r", encoding="UTF-8") as file:
                        df = pd.read_csv(file, sep=",", header=0,encoding="UTF-8")
                        print(pd.json_normalize(df["joint"]))
                        st.success("nice")
                        sleep(2)
                        st.rerun()
                else:
                    st.error("No data name given")
            except FileNotFoundError:
                st.error("Such no File exist")
            except Exception as e:
                st.error(f"Correct your data {e}")
    
    if select_action == "Json":
        data_name = st.text_input("Put the name of your file:")
        
        if not data_name.endswith(".json"):
            data_name += ".json"
            
        st.write("Import your data to a Json file")
        st.write("Press the button below to import the data to a jsono file")
        if st.button("IMport data"):
            try:
                if data_name != "":
                    st.write("Importing data...")
                    with open(data_name,"r", encoding="UTF-8") as file:
                        df = pd.read_json(file, orient="columns",encoding="UTF-8")
                        st.success("nice")
                        print(pd.json_normalize(df["joint"]))
                        sleep(2)
                        st.rerun()
                else:
                    st.error("No data name given")
            except FileNotFoundError:
                st.error("Such no File exist")
            except Exception as e:
                st.error(f"Correct your data {e}")