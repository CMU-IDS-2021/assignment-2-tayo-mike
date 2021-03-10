#
#
import streamlit as st
import pandas as pd
import altair as alt
from helper_func import*

#
#

Data_folder = "Dataset\\"

df = load_data(Data_folder)

#
#

st.write(df[1])
