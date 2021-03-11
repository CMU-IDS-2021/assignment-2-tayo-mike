import streamlit as st
import pandas as pd
import altair as alt

st.title("Let's analyze some Penguin Data 🐧📊.")

@st.cache  # add caching so we load the data only once
def load_data(data_file, file_type):
    if file_type == 'csv':
        return pd.read_csv(data_file)
    if file_type == 'excel':
        return pd.read_excel(data_file)

df1 = load_data("health_ineq_online_table_3.csv")
df2 = load_data("health_ineq_online_table_4.csv")
df3 = load_data("health_ineq_online_table_5.csv")

st.write("Let's look at raw data in the Pandas Data Frame.")

st.write(df1)
st.write(df2)
st.write(df3)

st.write("Hmm 🤔, is there some correlation between body mass and flipper length? Let's make a scatterplot with [Altair](https://altair-viz.github.io/) to find.")

# chart = alt.Chart(df).mark_point().encode(
#     x=alt.X("body_mass_g", scale=alt.Scale(zero=False)),
#     y=alt.Y("flipper_length_mm", scale=alt.Scale(zero=False)),
#     color=alt.Y("species")
# ).properties(
#     width=600, height=400
# ).interactive()

# st.write(chart)
