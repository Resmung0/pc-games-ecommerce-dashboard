from pandas import read_csv, to_numeric
import streamlit as st

@st.cache_data
def extract_nuuvem_data():
    dataframe = read_csv('data/raw/nuuvem.csv', parse_dates=['release_date'])
    return dataframe.assign(price=to_numeric(dataframe.price))



