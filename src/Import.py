import streamlit as st
import pandas as pd
import csv

def run():	
    st.title("Import your data")
    st.write("Import your data to a CSV file")

    select_action = st.selectbox("Select action", ["CSV", "Json"])
    data_name = st.text_input("Put the name of your file:")
    if select_action == "CSV":
        st.write("Import your data to a CSV file")
        df = pd.DataFrame({
            "A": [1, 2, 3, 4],
            "B": [5, 6, 7, 8]
        })
        st.write(df)
        st.write("Press the button below to export the data to a CSV file")
        if st.button("Imortdata"):
            st.write("Importing data...")
            with open(data_name, mode='r') as file:
                data = csv.DictReader(file) #jede zeile wird als dictonary eingelesen
                for row in data:
                    pass #noch zu überlegen ob es als eine liste oder in eine Dict zu speichern
            st.write("Data imported successfully")
    
    if select_action == "Json":
        pass