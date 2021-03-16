import streamlit as st
import pandas as pd
import altair as alt

st.title("Let's look at some social mobility data 📊.")
st.write("More particularly, let's see how income affects the life expectancy of Americans at a state level")

@st.cache  # add caching so we load the data only once
def load_data(data_file, file_type):
    if file_type == 'csv':
        return pd.read_csv(data_file)
    if file_type == 'excel':
        return pd.read_excel(data_file)

df1 = load_data("health_ineq_online_table_3.csv", "csv")
df2 = load_data("health_ineq_online_table_4.csv", "csv")
df3 = load_data("health_ineq_online_table_5.csv", "csv")
# df4 = load_data("health_ineq_online_table_3_perc.csv", "csv")

st.write("Here's the raw data we would be examining")

agg_data = df1[["statename", "le_agg_q1_F", "le_agg_q2_F", "le_agg_q3_F", "le_agg_q4_F", "le_agg_q1_M", "le_agg_q2_M", "le_agg_q3_M", "le_agg_q4_M"]]
agg_data["le_agg_F"] = agg_data[["le_agg_q1_F", "le_agg_q2_F", "le_agg_q3_F", "le_agg_q4_F"]].mean(axis=1)
agg_data["le_agg_M"] = agg_data[["le_agg_q1_M", "le_agg_q2_M", "le_agg_q3_M", "le_agg_q4_M"]].mean(axis=1)

# st.write(df1)
# st.write(df2)
st.write(agg_data)

# st.write("Hmm 🤔, is there some correlation between body mass and flipper length? Let's make a scatterplot with [Altair](https://altair-viz.github.io/) to find.")

# chart = alt.Chart(agg_data).mark_point().encode(
#     x=alt.X("statename", scale=alt.Scale(zero=False)),
#     y=alt.Y("le_agg_F", scale=alt.Scale(zero=False)),
#     color=alt.Y("statename")
# ).properties(
#     width=600, height=400
# ).interactive()

highlight = alt.selection(type='single', on='mouseover',
                          fields=['symbol'], nearest=True)

base = alt.Chart(df3).encode(
    x='year:T',
    y='le_agg_q4_F',
    color='statename'
)

points = base.mark_circle().encode(
    opacity=alt.value(0)
).add_selection(
    highlight
).properties(
    width=600
)

lines = base.mark_line().encode(
    size=alt.condition(~highlight, alt.value(1), alt.value(3))
)

st.write(points + lines)

a = alt.Chart(agg_data).mark_line(color='blue').encode(
    x='statename', y='le_agg_F')

b = alt.Chart(agg_data).mark_line(color='red').encode(
    x='statename', y='le_agg_M')

c = alt.layer(a, b)

st.altair_chart(c, use_container_width=True)

agg_data.index.name = "statename"
data = agg_data[["le_agg_q1_F", "le_agg_q2_F", "le_agg_q3_F", "le_agg_q4_F", "le_agg_q1_M", "le_agg_q2_M", "le_agg_q3_M", "le_agg_q4_M"]].reset_index().melt("statename")
chart = alt.Chart(data).mark_line().encode(
    x='statename',
    y='value',
    color='variable'
).properties(
    width=1000,
    height=400
)

st.write(chart)
