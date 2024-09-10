import streamlit as st
import pandas as pd
import numpy as np

@st.cache_data
def load_data(file_path='data/data.parquet'):
    df = pd.read_parquet(file_path)
    df['Asked Date'] = pd.to_datetime(df['Asked Date'])
    df['Modified Date'] = pd.to_datetime(df['Modified Date'])
    
    # Convert 'Views' to numeric, handling any non-numeric characters
    df['Views'] = df['Views'].replace(r'[^0-9]', '', regex=True)
    df['Views'] = pd.to_numeric(df['Views'], errors='coerce')
    
    df['Votes'] = pd.to_numeric(df['Votes'], errors='coerce')
    df['Number of Answers'] = pd.to_numeric(df['Number of Answers'], errors='coerce')
    df['Highest Score Answer Score'] = pd.to_numeric(df['Highest Score Answer Score'], errors='coerce')
    
    return df