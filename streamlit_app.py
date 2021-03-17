import streamlit as st
import pandas as pd
import altair as alt
from vega_datasets import data

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


st.write(agg_data)


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