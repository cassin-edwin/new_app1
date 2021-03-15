import streamlit as st
import pandas as pd 
import numpy as np 
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go 
import matplotlib.pyplot as plt 
import io
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS

Deliveries_url = ("deliveries.csv")
Matches_url = ("matches.csv")

st.image("https://www.searchpng.com/wp-content/uploads/2019/02/IPL-Logo-PNG.png", width=80)
st.sidebar.image("https://www.searchpng.com/wp-content/uploads/2019/02/IPL-Logo-PNG.png", width=80)
st.title("Data Visualization of IPL matches.") 
st.sidebar.title("Data Visualization of IPL matches.")
st.markdown("This application is a Streamlit dashboard used for Data Visualization of IPL matches played by any player selected from the menu.")
st.sidebar.markdown("This application is a Streamlit dashboard used for Data Visualization based on different parameters of IPL matches played by any player slected from the menu.")


@st.cache(persist = True)

def load_deliveries():
    data = pd.read_csv(Deliveries_url)
    return data

data = load_deliveries()



def load_matches():
    data2 = pd.read_csv(Matches_url)
    return data2

data2 = load_matches()

Cdata = data2.fillna("missing")




Cdata = Cdata['date'] = Cdata['date'].astype('datetime64[ns]')
Cdata = data2.sort_values(by = ['season'])

st.sidebar.markdown("Here visualizations are being done on two sets of data:")
st.sidebar.markdown("Source: cricsheet dataset posted on Kaggle")


if st.sidebar.checkbox("Show", True):
    Deliveries = st.sidebar.checkbox("Display Deliveries Data")
    if Deliveries:
        st.write(data.head(1000))

    Matches = st.sidebar.checkbox("Display Matches Data")
    if Matches:
        st.write(data2.head(1000))


    
summary = st.sidebar.radio('Data Statistics', ('Deliveries Dataset','Matches_Dataset'))


st.markdown("Data Statistics and Summary")
if summary == 'Deliveries Dataset':
    st.write(data.describe())
else:
    st.write(data2.describe())


players1 = st.sidebar.multiselect('Search/Choose any one batsman, to see visualizations from Deliveries dataset.', data['batsman'].unique())

new_data = data[(data['batsman'].isin(players1))]

st.markdown("<Kindly select any player from the sidebar>")

fig1 = px.bar(new_data, x='batsman' , y='batsman_runs', color= 'over')
fig1.update_layout(title_text = "Bar plot showing total runs in an over made by the selected player")
st.plotly_chart(fig1)

fig2 = px.scatter_matrix(new_data, dimensions=["wide_runs", "bye_runs", "legbye_runs", "noball_runs"], color="ball")
fig2.update_layout(title_text= "Scatter plot showing data on different parameters in all the matches played by the selected player")
st.plotly_chart(fig2)

fig3 = px.scatter(new_data, x="over", y="penalty_runs", size="batsman_runs", color="ball",
           hover_name="batsman", log_x=True, size_max=60)
fig3.update_layout(title_text= "This graph shows zero penalty runs in all the matches played by the selected player")           
st.plotly_chart(fig3)

st.markdown("### This Data visualization is from 'Matches dataset' of IPL matches played by MS Dhoni")
st.markdown("note:This Data visualization is already selected for 1 Player")

fig4 = px.treemap(Cdata.query('season == 2017'), path=[px.Constant('player_of_match'), 'venue', 'winner'], values = 'win_by_runs', color = 'player_of_match', hover_data= ['date'])
fig4.update_layout(title_text = "Tree map showing players of the matches in different IPL teams")
st.plotly_chart(fig4)

fig5 = px.area(Cdata[(Cdata.player_of_match == "MS Dhoni")], x = "season" , y = "win_by_wickets", color="date", line_group="city")
fig5.update_layout(title_text = "Area chart showing matches won by MS Dhoni in different seasons")
st.plotly_chart(fig5)

fig6 = px.scatter(Cdata[(Cdata.player_of_match == "MS Dhoni")], x= "win_by_runs", y = "season", size = "win_by_runs", color = "venue" , hover_name = "player_of_match", log_x =True, size_max = 60)
fig6.update_layout(title_text="Scatter plot showing wins_by_runs data over a season per se by MS Dhoni")
st.plotly_chart(fig6)

fig7 = px.density_heatmap(Cdata[(Cdata.player_of_match == "MS Dhoni")], x = "season", y = "city", marginal_x = "rug", marginal_y="histogram")
fig7.update_layout(title_text = "Density Heat Map depicting matches played in different cities over the years")
st.plotly_chart(fig7)

fig8 = px.scatter(Cdata[(Cdata.player_of_match == "MS Dhoni")], y= "toss_winner", x="season", color="city")
fig8.update_layout(title_text = "This plot depicts, MS Dhoni's IPL team Chennai Super Kings are six time toss winners")
st.plotly_chart(fig8)

st.sidebar.header("Word Cloud")
if st.sidebar.checkbox("Open", True, key='3'):
    st.sidebar.markdown("Select open to see word cloud for IPL teams.")
    words = ' '.join(data['batting_team'].unique())
    processed_words = ' '.join([word for word in words.split()])
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', width=800, height=640).generate(processed_words)
    fig9, ax = plt.subplots()
    plt.imshow(wordcloud)
    plt.xticks([])
    plt.yticks([])
    st.pyplot(fig9)
 






st.markdown("Project made by Fatima Majid using Streamlit")
