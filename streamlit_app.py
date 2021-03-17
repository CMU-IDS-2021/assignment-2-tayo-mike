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

st.write("Here's the raw data we would be examining")

agg_data = df1[["statename", "le_agg_q1_F", "le_agg_q2_F", "le_agg_q3_F", "le_agg_q4_F", "le_agg_q1_M", "le_agg_q2_M", "le_agg_q3_M", "le_agg_q4_M"]]
agg_data["le_agg_F"] = agg_data[["le_agg_q1_F", "le_agg_q2_F", "le_agg_q3_F", "le_agg_q4_F"]].mean(axis=1)
agg_data["le_agg_M"] = agg_data[["le_agg_q1_M", "le_agg_q2_M", "le_agg_q3_M", "le_agg_q4_M"]].mean(axis=1)

fin_data = agg_data[["statename", "le_agg_F", "le_agg_M"]]

le_timeseries_for_states = {}
states = agg_data["statename"]
for state in states:
    state_data = df3[df3["statename"] == state]
    state_data["le_agg_F"] = state_data[["le_agg_q1_F", "le_agg_q2_F", "le_agg_q3_F", "le_agg_q4_F"]].mean(axis=1)
    state_data["le_agg_M"] = state_data[["le_agg_q1_M", "le_agg_q2_M", "le_agg_q3_M", "le_agg_q4_M"]].mean(axis=1)
    state_data = state_data[["year", "le_agg_F", "le_agg_M"]]
    le_timeseries_for_states[state] = state_data

alabama = le_timeseries_for_states['Alabama']
alabama = alabama.melt('year')

st.write(alt.Chart(alabama).mark_line().encode(
    x='year:O',
    y='value',
    color='variable:N',
    # column='site:N'
)
)

st.write ("Here's our raw data")
st.write(agg_data)
st.write("\n")
st.write(df3)

st.write("Let's see the life expectancy for each state - Male and Female at a glance")

# agg_data.index.name = "statename"
data = agg_data[["statename", "le_agg_q1_F", "le_agg_q2_F", "le_agg_q3_F", "le_agg_q4_F", "le_agg_q1_M", "le_agg_q2_M", "le_agg_q3_M", "le_agg_q4_M"]].melt("statename")
chart = alt.Chart(data).mark_bar().encode(
    x=alt.X('statename', title="States"),
    y=alt.Y('sum(value)', title="Life Expectancy at Income Quartiles"),
    color='variable',
    tooltip='mean(value)'
).properties(
    width=1000,
    height=400
)

st.write(chart)



st.write ("Next, we see the average life expectancy across all income quartiles by gender")

options = []
options = list(agg_data["statename"])

input_dropdown = alt.binding_select(options=options)
selection = alt.selection_single(fields=['statename'], bind=input_dropdown, name='statename')
color = alt.condition(selection,
                    alt.Color('statename:N', legend=None),
                    alt.value('lightgray'))

chart = alt.Chart(agg_data).mark_bar().encode(
    x=alt.X("statename"),
    y=alt.Y("le_agg_M"),
    color="statename",
    tooltip='statename:N'
).properties(
    width=1000,
    height=400
)

st.write(chart)

chart2 = alt.Chart(agg_data).mark_bar().encode(
    x=alt.X("statename"),
    y=alt.Y("le_agg_F"),
    color="statename",
    tooltip='statename:N'
).properties(
    width=1000,
    height=400
)

st.write(chart2)

####### Chart 2############

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
).interactive().add_selection(
    selection
)

lines = base.mark_line().encode(
    size=alt.condition(~highlight, alt.value(1), alt.value(3))
).interactive().add_selection(
    selection
)

st.write(points + lines)