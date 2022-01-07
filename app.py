from pandas.io.parsers import read_csv
import streamlit as st
import pandas as pd
import numpy as np

from PIL import Image

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# import re
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import *
import datetime as dt
from matplotlib.ticker import MaxNLocator
# import regex
# import emoji
from seaborn import *
# from heatmap import heatmap
from wordcloud import WordCloud , STOPWORDS , ImageColorGenerator
from nltk import *
from plotly import express as px



img = Image.open("choice_design.png")
# st.title("Choice Coin Discord Chat Analysis.")
st.markdown("<h1 style='text-align: center;'>Choice Coin Discord Chat Analysis</h1>", unsafe_allow_html=True)
st.image(img)
st.markdown("<h3 style='text-align: center;'>Chats analysis from ⏱ Tuesday 29th June until Friday Dec 31st 2021 </h3>", unsafe_allow_html=True)
# st.write("2021 Wrapped.")



# ?#############################################################
@st.cache(allow_output_mutation=True)
def read_df():
    data = []
    main_df = pd.read_csv("clean.csv")
    data.append(main_df)

    emoji = pd.read_csv("emoji.csv")
    data.append(emoji)
    return data

data = read_df()
df = data[0]
emoji_ = data[1]

st.header("Totals")
st.markdown("<h2 style='text-align: center;'>☀️🌘Total Number of Days: 186 </h2>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>📩📩Total Number of Messages Sent: 33168 </h2>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>🙍🏽🙍‍♀️Number of Unique Authors: 2451 </h2>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>💬💬Number of Word: 1382808 </h2>", unsafe_allow_html=True)

# st.markdown(
#                 """
#                 ... Days Total .. |... Unique Authors ... |... Message Total ... |... Words Total ...
#                 ----------------|--------------|------------|----------
#                 {0}             | {1}          | {2}        | {3} 
#                 """.format(100, 100, 100, 100)
#         )
st.text("")
st.text("")
st.text("")



# ?#############################################################
st.subheader("Word Cloud")
st.write("Most used words on the discord channel, The words \"Choice\" and \"Choice Coin\" standing out")

df["Message"] = df.Message.apply(str)
# text = " ".join(review for review in df.Message)
# wordcloud = WordCloud(width=1000, height=500, background_color="white").generate(text)
# Open a plot of the generated image.
plt.figure( figsize=(24,12), facecolor='k')
# plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad=0)
# st.pyplot(plt)
img2 = Image.open("wordcloud__.jpg")
st.image(img2)

st.text("")
st.text("")
st.text("")
st.text("")


# ?#############################################################
st.subheader("Messages Sent Per Day")
st.write("8000+ Messages sent on October 24, Not sure what event happened that day.")

date_df = df.Date.value_counts().rename_axis('Date').reset_index(name='Value').sort_values(by = "Date")
fig = px.line(date_df, x='Date', y="Value", width=1000, height=500)
fig.update_layout( 
                            legend_orientation='h', margin=dict(l=0, r=0, t=0, b=0),
                            width=800,height=300)
# st.plotly_chart(fig,use_container_width=True)

# fig = go.Figure(data=go.Scatter(x= date_df["Date"], y=date_df['Value']))
# fig.update_layout(title_text='Message Trend',
#                             legend_orientation='h', margin=dict(l=0, r=0, t=0, b=0),
#                             width=700,height=400,
#                             xaxis_title='Date',
#                             yaxis_title='No of Messages')
st.plotly_chart(fig, use_container_width= True)
st.text("")
st.text("")
st.text("")
st.text("")


# ?#############################################################
df["Date_Col"] = pd.to_datetime(df["Date_Col"])

df_1 = df.copy()
df_1["hours"] = df_1['Date_Col'].apply(lambda x: x.hour)
times_df = df_1.groupby('hours').count().reset_index().sort_values(by = 'hours')

st.subheader("Most Active Hours.")
st.write("There\'s always more activity in the evening/night mostly between (8pm - 12am).")

plt.rcParams['font.size'] = 15
fig = plt.figure(figsize=(24, 12))
# plt.rcParams['figure.figsize'] = (20, 8)
sns.set_style("darkgrid")
plt.rcParams['font.size'] = 26
# plt.title('Most active hour of the day');
time_plot = sns.barplot(x="hours",y="Message",data = times_df,dodge=False)
labels=["12:AM","01:AM","02:AM","03:AM","04:AM","05:AM","06:AM","07:AM","08:AM","09:AM","10:AM","11:AM","12:PM","01:PM","02:PM","03:PM","04:PM","05:PM","06:PM","07:PM","08:PM","09:PM","10:PM","11:PM"]
time_plot.set_xticklabels(rotation=15, labels=labels)
# time_plot.bar_label(time_plot.containers[0])
plt.xticks([i for i in range(24)], labels=labels, rotation=70)
plt.ylabel("No of Messages")
st.pyplot(fig)

st.text("")
st.text("")
st.text("")
st.text("")


# ?#############################################################

st.subheader("Most Active Days in 2021.")
st.write("Some days in the year that recorded the most activities.")
df.Date = pd.to_datetime(df.Date).dt.date

# st.table(df.groupby('Date').sum())
# plt.figure(figsize = (24, 12))
grouped_by_date = df.groupby('Date').count().reset_index().sort_values(by = 'Message', ascending = False).head(15)
grouped_by_date['day_sent'] = grouped_by_date['Date'].apply(lambda x: x.strftime('%a'))
ax = sns.barplot(y = 'Message', x = 'Date', data = grouped_by_date)

# I spent way too long to get the bar annotations to work properly. Thank you again, StackOverflow.
for bar, label in zip(ax.patches, grouped_by_date['day_sent']):
    x = bar.get_x()
    width = bar.get_width()
    height = bar.get_height()
    ax.text(x + width/2., height + 10, label, ha="center") 

ax.set_xticklabels(ax.get_xticklabels(), rotation = 80)
# plt.title('Most Active Days')
st.pyplot(plt)

st.text("")
st.text("")
st.text("")
st.text("")

# ?#############################################################
df['Mon'] = df['Date_Col'].dt.month
months = {
    1 : 'Jan',
    2 : 'Feb',
    3 : 'Mar',
    4 : 'Apr',
    5 : 'May',
    6 : 'Jun',
    7 : 'Jul',
    8 : 'Aug',
    9 : 'Sep',
    10 : 'Oct',
    11 : 'Nov',
    12 : 'Dec'
}
df['Month'] = df['Mon'].map(months)
df.drop('Mon',axis=1,inplace=True)

month = df.Month.value_counts().rename_axis('Month').reset_index(name='Message')

st.subheader("Total Messages Sent (grouped by month)")
st.write("October and December happen to be the month with the most activity")

fig = px.bar(month, x='Month', y='Message',
            hover_data=['Message'], color='Message',
            labels={'Message':'No of Messages'}, height=500, color_continuous_scale = "Agsunset", text= "Message")
fig.update_coloraxes(showscale=False)
fig.update_layout( 
                            legend_orientation='h', margin=dict(l=0, r=0, t=0, b=0),
                            width=800,height=400)

st.plotly_chart(fig, use_container_width=True)


st.text("")
st.text("")
st.text("")
st.text("")

# ?#############################################################

st.subheader("Total Message Sent (grouped by day)")
dow = df.Day.value_counts().rename_axis('Day').reset_index(name='Message').sort_values(ascending= False, by= "Message")

fig = px.bar(dow.head(20), x='Day', y='Message',
            hover_data=['Message'], color='Message',
            labels={'Message':'No of Messages'}, height=500, color_continuous_scale = "Agsunset", text= "Message"
        )
fig.update_layout(
                            legend_orientation='h', margin=dict(l=0, r=0, t=0, b=0),
                            width=800,height=400)
fig.update_coloraxes(showscale=False)
st.plotly_chart(fig,use_container_width=True)

st.text("")
st.text("")
st.text("")
st.text("")

# ?#############################################################
st.subheader("Most Active Members of the Channel")
author = df.Author.value_counts().rename_axis('Author').reset_index(name='Message').sort_values(ascending= False, by= "Message")
fig = px.bar(author.head(20), x='Author', y='Message',
            hover_data=['Message'], color='Message',
            labels={'Message':'No of Messages'}, height=450, color_continuous_scale = "Agsunset", text= "Message"
            )
fig.update_layout(
                            legend_orientation='h', margin=dict(l=0, r=0, t=0, b=0),
                            width=800,height=400)
fig.update_coloraxes(showscale=False)
st.plotly_chart(fig,use_container_width=True)


st.text("")
st.text("")
st.text("")
st.text("")


# ?#############################################################
st.subheader("Most Url/Link Sent By User")
max_words = df[['Author','Url_Count']].groupby('Author').sum()
m_w = max_words.rename_axis('Author').reset_index().sort_values(by = "Url_Count", ascending= False)

fig = px.bar(m_w.head(10), x='Author', y='Url_Count',
            hover_data=['Url_Count'], color='Url_Count',
            labels={'Url_Count':'No of Urls'}, height=500, color_continuous_scale = "Agsunset", text= "Url_Count"
            )
fig.update_layout( 
                            legend_orientation='h', margin=dict(l=0, r=0, t=0, b=0),
                            width=800,height=400)
fig.update_coloraxes(showscale=False)
st.plotly_chart(fig, use_container_width=True)

st.text("")
st.text("")
st.text("")
st.text("")


# ?#############################################################
st.subheader("Most Used Emoji in Channel")
st.write("🚀🚀🚀  😂😂😂 are the most frequent emoji used by members")
fig = px.pie(emoji_, values='number_of_Emoji', names='emoji')
fig.update_traces(textposition='inside', textinfo='percent+label')
fig.update_layout( 
                            margin=dict(l=0, r=0, t=0, b=0),
                            width=800,height=400)
# fig.update_coloraxes(showscale=False)
st.plotly_chart(fig, use_container_width=True)



st.subheader("About this App:")
st.markdown(
        """
        
        **Data Scientist / Developer:** [Paul Okewunmi](https://linkedin.com/in/paul-okewunmi-a24526171). """
    )