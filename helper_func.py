import streamlit as st
import pandas as pd
import os
import fnmatch

@ st.cache
def load_data(Data_folder = "."):

    fn = list()

    for filename in os.listdir(Data_folder):
        if fnmatch.fnmatch(filename,'*.csv'):
            fn.append(pd.read_csv(Data_folder + filename))
    
    return fn 

def test():
    print("test")