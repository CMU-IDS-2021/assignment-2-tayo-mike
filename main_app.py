#
#
import streamlit as st
import pandas as pd
import altair as alt
from vega_datasets import data
from helper_func import*

#
#

Data_folder = "Dataset\\"

df = load_data(Data_folder)

#
#

st.write(df[0])

#US State Background

states = alt.topo_feature(data.us_10m.url, feature ='states')

Background = alt.Chart(states).mark_geoshape(
    fill = 'lightgray',
    stroke = 'black'
).properties(
    width=500,
    height=300
).project('albersUsa')

points = alt.Chart()

Background
