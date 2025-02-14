import streamlit as st
import pandas as pd

def run():	
    st.title("Export your data")
    st.write("Export your data to a CSV file")

    select_action = st.selectbox("Select action", ["CSV", "Json"])
    data_name = st.text_input("Put the name of your file:")
    if select_action == "CSV":
        st.write("Export your data to a CSV file")
        df = pd.DataFrame({
            "A": [1, 2, 3, 4],
            "B": [5, 6, 7, 8]
        })
        st.write(df)
        st.write("Press the button below to export the data to a CSV file")
        if st.button("Export data"):
            st.write("Exporting data...")
            df.to_csv(data_name, index=False, header=tr)
            st.success("A CSV-File created successfully")
    if select_action == "Json":
        pass

    