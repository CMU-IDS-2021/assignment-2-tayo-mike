import streamlit as st
import pandas as pd
import altair as alt
from vega_datasets import data

st.title("Let's look at some social mobility data 📊.")
st.write("More particularly, let's see how income affects the life expectancy of Americans at a state level")

st.subheader("These are our goals: ")
st.write("1. We set out to investigate the male life expectancy in all states +\n"
        "2. We set out to investigate the female life expectancy in all states +\n"
        "3. We set out to investigate the life expectancy as a time series between 2001 and 2014 across all states in the United States")

st.subheader("Here are our findings: ")
st.write("We came to find that generally, across the United States, the life expectancy is higher for women. We also found that the life expectancy is also highest for the population earning in the 4th percentile of their income bracket. I think this is a very logical trend because as with the typical world bank indicators studies, we find that generally, when people earn more, they tend to have a better quality of life which can be linked to improved health and ultimately, a higher life expectancy. Also, as generally, men tend to take on more tedious roles in society - heavy lifting and highly demanding blue-collar jobs, it is almost of no surprise that the life expectancy for men is lower than that of women across all income quartiles. +\n"

"Also, it is very worthy to note that analysing data at the States level is not the best as we found, rather harshly that due to the very small amount of data observed at the state level, meaningful insights or trends or seasonality are hard to come by and as such, some measures to be taken when faced with a similar scenario would be getting more data,, preferably at County level for greater observations or merging the data at state level with some other indicators so that at the very least, the dimensionality of exploratory analysis is greater than the initial data received.")

@st.cache  # add caching so we load the data only once
def load_data(data_file, file_type):
    if file_type == 'csv':
        return pd.read_csv(data_file)
    if file_type == 'excel':
        return pd.read_excel(data_file)

df1 = load_data("health_ineq_online_table_3.csv", "csv")
df2 = load_data("health_ineq_online_table_4.csv", "csv")
df3 = load_data("health_ineq_online_table_5.csv", "csv")
# df4 = load_data("nst-est2019-alldata.csv", "csv")

# st.write(df4)

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
# alabama_ =pd.DataFrame(columns = ["Male", "Female"])
# alabama_male = alabama["le_agg"]
alabama = alabama.melt('year')
# alabama = alabama.groupby

# st.write(alt.Chart(alabama).mark_line().encode(
#     x='year:O',
#     y='value',
#     color='variable:N',
#     # column='site:N'
# )
# )

st.write ("Here's our raw data")
st.write(agg_data)
st.write("\n")
st.write(df3)

st.write("Let's see the life expectancy for each state - Male and Female at a glance. Each section is selectable")

# agg_data.index.name = "statename"
data = agg_data[["statename", "le_agg_q1_F", "le_agg_q2_F", "le_agg_q3_F", "le_agg_q4_F", "le_agg_q1_M", "le_agg_q2_M", "le_agg_q3_M", "le_agg_q4_M"]].melt("statename")
selector = alt.selection_single(encodings=['x', 'color'])
chart = alt.Chart(data).mark_bar().encode(
    x=alt.X('statename', title="States"),
    y=alt.Y('sum(value)', title="Life Expectancy at Income Quartiles"),
    # color='variable',
    color=alt.condition(selector, 'variable', alt.value('lightgray')),
    tooltip=["variable",'mean(value)']
)
# st.write(agg_data)


highlight = alt.selection(type='single', on='mouseover',fields=['symbol'], nearest=True)

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
    width=1000,
    height=400
).add_selection(
    selector
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
    tooltip=['statename:N', "le_agg_M"]
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

st.write("Next, we see the distribution of the life expectancies on the map across all states")

st.write(chart)


###
#
###

## use airport data for lat and long of map background
airports = data.airports()
airports = airports[["state","latitude","longitude"]]
state_loc = airports.groupby(['state']).mean()

source = df3
source["state"] = source["stateabbrv"]
source = source.set_index('state').join(state_loc)

source["index"] =  list(range(len(source))) 
source = source.set_index('index')

## data that will be considered
source["state"] = source["statename"]
source["Female, Income: Q1"] = source["le_agg_q1_F"]
source["Female, Income: Q2"] = source["le_agg_q2_F"]
source["Female, Income: Q3"] = source["le_agg_q3_F"]
source["Female, Income: Q4"] = source["le_agg_q4_F"]

#US State Background # https://altair-viz.github.io/gallery/airports_count.html
states = alt.topo_feature(data.us_10m.url, feature ='states')
Background = alt.Chart(states).mark_geoshape(
    fill = 'lightgray',
    stroke = 'black'
).properties(
    width=500,
    height=300
).project('albersUsa')

# year slider for Maps
slider = alt.binding_range(min = source['year'].min(), max = source['year'].max(), step =1)
select_year = alt.selection_single(name="year", fields=['year'], bind = slider, init={'year':source['year'].min()})

base = alt.Chart(source)

### trend line plot 

plot=base.mark_point(filled=True   
).encode(
    alt.X('year:O', scale = alt.Scale(zero=False) ),
    alt.Y('average(Female, Income: Q1):Q', scale = alt.Scale(zero=False)),
    color=alt.value("salmon")
)

plot+=base.mark_point(filled =True   
).encode(
    alt.X('year:O', scale = alt.Scale(zero=False) ),
    alt.Y('average(Female, Income: Q2):Q', scale = alt.Scale(zero=False)),
    color=alt.value("salmon"),
    shape = alt.value("cross")
)

plot+=base.mark_point(filled =True  
).encode(
    alt.X('year:O', scale = alt.Scale(zero=False) ),
    alt.Y('average(Female, Income: Q3):Q', scale = alt.Scale(zero=False)),
    color=alt.value("salmon"),
    shape = alt.value("square")
)

plot+=base.mark_point(filled=True 
).encode(
    alt.X('year:O', scale = alt.Scale(zero=False) ),
    alt.Y('average(Female, Income: Q4):Q', scale = alt.Scale(zero=False), axis=alt.Axis(title='Average Female Age')),
    
    color=alt.value("salmon"),
    shape = alt.value("diamond"),
    legend=alt.value(legend=alt.Legend)

)


### map plots for the 4 Q


points_Female1 = base.mark_circle().encode(
    longitude = "longitude:Q",
    latitude = "latitude:Q",

    size = alt.Size("Female, Income: Q1:Q", scale=alt.Scale(zero=False), legend=None),
    color = alt.value("salmon"),
    tooltip = ["state:N","Female, Income: Q1:Q"]
  ).add_selection(
      select_year,
      
  ).transform_filter(
      select_year   
  ).properties(title='Q1')

points_Female2 = base.mark_circle().encode(
    longitude = "longitude:Q",
    latitude = "latitude:Q",

    size = alt.Size("Female, Income: Q2:Q",scale=alt.Scale(zero=False), legend=None),
    color = alt.value("salmon"),
    tooltip = ["state:N","Female, Income: Q2:Q"]
  ).add_selection(
      select_year
      
  ).transform_filter(
      select_year   
  ).properties(title='Q2')

points_Female3 = base.mark_circle().encode(
    longitude = "longitude:Q",
    latitude = "latitude:Q",

    size = alt.Size("Female, Income: Q3:Q",scale=alt.Scale(zero=False), legend=None),
    color = alt.value("salmon"),
    tooltip = ["state:N", "Female, Income: Q3:Q"]
  ).add_selection(
      select_year
      
  ).transform_filter(
      select_year   
  ).properties(title='Q3')

points_Female4 = base.mark_circle().encode(
    longitude = "longitude:Q",
    latitude = "latitude:Q",

    size = alt.Size("Female, Income: Q4:Q",scale=alt.Scale(zero=False), legend=None),
    color = alt.value("salmon"),
    tooltip = ["state:N","Female, Income: Q4:Q"]
  ).properties(title = '').add_selection(
      select_year
      
  ).transform_filter(
      select_year   
  ).properties(title='Q4')

Maps = (points_Female1 | points_Female2) & (points_Female3|points_Female4)

st.write(Maps)
st.write(plot)
