## Importing the libraries.
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


## Adding the header or title
st.header("Covid-19 WorldWide Case Tracker")

## Using this to add a newline
st.markdown(' ')

st.markdown("The virus which took the whole world by surprise. Its causing huge damage to humanity unlike anything in the living memory.")

## Using this to add a newline
st.markdown(' ')

st.markdown('It is been more than 4 months now since the first case was noticed and it is still growing in lot of countries. Few countries have lost large number of people to this deadly virus and some countries have not been impacted a lot in terms of lives. But the economic impact of this virus is big for every single country and vast majority of the human population. This has killed the livelihood of huge population of the world. There will be lot of people dying out of hunger because of all these lockdowns in poor and developing countries.')

## load the data
countries = pd.read_csv("https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv")

## Select the Companies 
country = st.sidebar.selectbox(
	"Select the Country ::",
	(list(countries.loc[:,'Country'].unique()))
)

## Adding text on the sidebar
st.sidebar.markdown("Data Source:: Johns Hopkins University Center for Systems Science and Engineering")

## Filter the data
data = countries[countries['Country'] == country]

st.subheader("Daily Case Numbers")


### Daily Line Graph
fig = go.Figure()
fig.add_trace(go.Scatter(x = data['Date'], y = data['Confirmed'], name = "Confirmed Cases", marker={"color" :"#34495E"}))
fig.add_trace(go.Scatter(x = data['Date'], y = data['Recovered'], name = "Recovered Cases", marker={"color" :"#1E56C1"}))
fig.add_trace(go.Scatter(x = data['Date'], y = data['Deaths'], name = "Deaths", marker={"color" :"#E5C826"}))
fig.update_xaxes(rangeslider_visible=True)
fig.update_layout(width=800, height=600)
st.plotly_chart(fig)


st.subheader("Status of the cases")

## Pie Chart
fig = go.Figure()
pied = data[data['Date'] == max(data['Date'])]
pied['Active'] = pied['Confirmed'] - pied['Recovered'] - pied['Deaths']
pied = pied.transpose().reset_index().iloc[3:]
pied.columns = ['Type', "TotalCases"]
fig = go.Figure(data=[go.Pie(labels=pied['Type'], 
                             values=pied['TotalCases'], 
                             hole=.3, 
                             marker={"colors" : ["#1E56C1","#E5C826","#34495E"]})])
st.plotly_chart(fig)


st.subheader("Cumulative Numbers")

## Cumulative Graph
fig = go.Figure(data=[
    go.Bar(name='Active', x=data['Date'], y=data['Confirmed'] - data['Recovered'] - data['Deaths'], marker={"color" :"#34495E"}),
    go.Bar(name='Recovered', x=data['Date'], y=data['Recovered'], marker={"color" :"#1E56C1"}),
    go.Bar(name='Deaths', x=data['Date'], y=data['Deaths'], marker={"color" :"#E5C826"})
])
# Change the bar mode
fig.update_layout(barmode='stack', width=800, height=600)
fig.update_xaxes(rangeslider_visible=True)
st.plotly_chart(fig)