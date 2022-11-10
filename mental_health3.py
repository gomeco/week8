#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import plotly.express as px
import geopandas as gpd
import folium
import numpy as np
import seaborn as sns
import plotly.express as px
import io
import streamlit as st
from streamlit_folium import folium_static



# In[2]:


df=pd.read_csv("https://raw.githubusercontent.com/gomeco/week8/main/survey.csv")


# In[3]:


#df["comments"].unique()


# In[4]:


#df["work_interfere"].unique()


# In[5]:


#df["leave"].unique()


# In[6]:


#df.Age.agg(['min','max'])


# # Data cleanen

# In[7]:


drop_neg = df.drop(df[df['Age'] <18].index, inplace=True)
drop_pos = df.drop(df[df['Age'] > 65].index, inplace=True)


# In[8]:


df.Age.agg(['min','max'])


# #Kolom gender cleanen hieronder

# In[9]:


df1=df.replace(dict.fromkeys(['M','male','Male-ish','maile', 'something kinda male?', 
                          'Mal', 'Male (CIS)', 'Make', 'Guy (-ish) ^_^', 'male leaning androgynous',
                          'msle', 'Mail', 'cis male', 'Malr', 'Cis Man', 
                          'ostensibly male', 'm', 'Cis Male', 'Male ', 'Man', 'ostensibly male, unsure what that really means'], 'Male'))
#df1.head(5)


# In[10]:


df2=df1.replace(dict.fromkeys(['female','f', 'F', 'Woman', 'queer/she/they', 'Femake', 'woman', 
                          'Female ', 'cis-female/femme', 'Female (cis)', 'femail', 'Cis Female'], 'Female'))
#df2


# In[11]:


df3= df2.replace(dict.fromkeys(['Trans-female', 'Trans woman', 'Female (trans)', 'non-binary', 
                          'Neuter', 'unsure what that really means', 'queer', 'Genderqueer', 
                          'Androgyne', 'fluid', 'Enby','Nah', 'Agender'], 'Other'))

#df3.head()


# In[12]:


df3["Gender"].unique()


# In[13]:


df3["Age"].unique()


# In[14]:


df3['no_employees'].value_counts()


# In[15]:


df4=df3.replace(dict.fromkeys(['More than 1000'], 5000))
df5=df4.replace(dict.fromkeys(['500-1000'], 1000))
df6=df5.replace(dict.fromkeys(['100-500'], 500))
df7=df6.replace(dict.fromkeys(['26-100'], 100))
df8=df7.replace(dict.fromkeys(['6-25'], 25))
df9=df8.replace(dict.fromkeys(['1-5'], 5))


df9['no_employees'].value_counts()


# # Data inspectie

# In[16]:


df3["Gender"].value_counts()


# In[17]:


df3["treatment"].value_counts()


# In[18]:


treatment_gender1=df3.loc[(df3['treatment'] == "Yes") & (df3['Gender'] == "Male")]
#treatment_gender1


procent_m=450*100/990
roundedNumber1 = round(procent_m, 2)

print("In totaal hebben " + str(roundedNumber1) + 
      " % van de mannen hulp gezocht voor een mentale aandoening binnen een IT bedrijf")


# In[19]:


treatment_gender2=df3.loc[(df3['treatment'] == "Yes") & (df3['Gender'] == "Female")]
#treatment_gender2

procent_f=170*100/247
roundedNumber2 = round(procent_f, 2)

print("In totaal hebben " + str(roundedNumber2) + 
      " % van de vrouwen hulp gezocht voor een mentale aandoening binnen een IT bedrijf")


# In[20]:


treatment_gender3=df3.loc[(df3['treatment'] == "Yes") & (df3['Gender'] == "Other")]
#treatment_gender3

procent_o=11*100/13
roundedNumber3 = round(procent_o, 2)

print("In totaal hebben " + str(roundedNumber3) + 
      " % van Other (geslacht) hulp gezocht voor een mentale aandoening binnen een IT bedrijf")


# In[21]:


#df3["Country"].value_counts()


# In[22]:


country_filter=df3.groupby('Country').filter(lambda x : len(x)>=10)
country_filter['Country'].value_counts()


# In[23]:


#Stap 1: Inspecteren in welke landen de meeste werknemers mentale hulp zoeken

treatment_country=country_filter.loc[(country_filter['treatment'] == "Yes")]
treatment_country["Country"].value_counts()


# # Slider met boxplot en scatter

# In[24]:


# Slider met boxplot

fig = px.box(  data_frame=df9,  x='treatment',   y='no_employees',  color='Gender', 
                 animation_frame='Country'
                 
                  ,
            labels={"no_employees": "Aantal werknemers in bedrijf",
                     "treatment": "Hulp zoekend voor mentale aandoening (Y/N)",
                     "Country": "Land",
                    "Gender": "Geslacht",
                 },
                title="Geslachten hulpzoekend mentale problemen gebaseerd op aantal werknemers bedrijf")
fig['layout'].pop('updatemenus')
fig.show()

st.plotly_chart(fig, use_container_width=True)


# In[25]:


#df9.info()


# In[26]:


# Slider met scatter

fig = px.scatter(  data_frame=df9,  x='Age',   y='Gender',  color='leave', 
                 animation_frame='Country'
                 
                  ,
            labels={"leave": "Moeilijkheid vertrekken",
                     "Age": "Leeftijd",
                     "Country": "Land",
                    "Gender": "Geslacht",
                 },
                title="titel bedenken")
fig['layout'].pop('updatemenus')
fig.show()


st.plotly_chart(fig, use_container_width=True)


# # Histogrammen

# In[27]:


#Hoevaak leeftijd voorkomt
fig = px.histogram(x=df9['Age'])

fig.update_layout(title='Hoevaak een leeftijd voorkomt')
fig.update_xaxes(title='Leeftijden')
fig.update_yaxes(title='Hoeveelheid')

fig.show()
st.plotly_chart(fig, use_container_width=True)


# In[28]:


#Hoevaak geslacht voorkomt
fig = px.histogram(x=df9['Gender'])

fig.update_layout(title='Hoevaak een gender voorkomt in Tech bedrijf')
fig.update_xaxes(title='Gender')
fig.update_yaxes(title='Hoeveelheid')

fig.show()
st.plotly_chart(fig, use_container_width=True)


# In[29]:


#Hoevaak geslacht voorkomt
fig = px.histogram(x=df9['family_history'])

fig.update_layout(title='Hoevaak een mentale aandoening in de familie voorkomt bij werknemers')
fig.update_xaxes(title='Mentale aandoening in de familie (Ja/Nee)')
fig.update_yaxes(title='Hoeveelheid')

fig.show()
st.plotly_chart(fig, use_container_width=True)


# # Boxplots

# In[30]:


fig = px.box(df9, x="Gender", y="Age", color="treatment",
            #category_orders={"job_titles": ["Data Scientist", "Data Engineer", "Data Analyst", 
             #                               "Machine Learnin Analyst", "Research Scientist", 
              #                              "Data Science Manager", "Data Architect"]},
            #labels={
             #        "job_title": "Baan titel",
              #       "salary_in_euro": "Salaris in Euro",
               #      "job_title": "Baan titel"
                # },
                title="Gemiddelde leeftijd per geslacht")
            



fig.show()
st.plotly_chart(fig, use_container_width=True)


# In[31]:


df_countries = pd.read_csv('https://raw.githubusercontent.com/gomeco/week8/main/countries.csv')


# In[32]:


df_compare = df9.merge(df_countries, left_on = "Country", right_on = "name")


# In[33]:


df_compare['Timestamp'] = pd.to_datetime(df_compare['Timestamp'])


# In[34]:


df_compare['year'] = df_compare['Timestamp'].dt.year


# In[35]:


df_compare['year'].value_counts()


# In[36]:


df_compare.info()


# In[37]:


gdf = gpd.GeoDataFrame(
    df_compare, geometry=gpd.points_from_xy(x=df_compare.longitude, y=df_compare.latitude, crs="EPSG:4326"))


# In[38]:


#countries_polygonen = geopandas.read_file('countries.geojson')


# In[39]:


#m = folium.Map(location = [df_compare['latitude'].mean(),df_compare['longitude'].mean()], zoom_start=2, control_scale=True)
#folium.GeoJson(data=countries_polygonen["geometry"]).add_to(m)
#m


# In[40]:


#folium_static(m)


# In[41]:


import http.client
import pandas as pd
conn = http.client.HTTPSConnection("data.cdc.gov")

headers = {}

conn.request("GET", "/resource/9j2v-jamp.csv?$$app_token=uNOBCZDlRBo1hcMQEtpOiMcGm&$limit=999999", headers=headers)
#token: WxRl58VIg5ybQ2cyCdTHcaUjE
res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))


# In[42]:


df_suicide_us = pd.read_csv(io.StringIO(data.decode("utf-8")), low_memory=False)


# In[43]:


df_suicide_us['year'].unique()


# In[44]:


df_suicide_us_2014 = df_suicide_us[df_suicide_us['year']==2014]


# In[45]:


df_suicide_us['stub_name'].unique()


# In[46]:


df_filtered_us = df_suicide_us_2014[df_suicide_us_2014['stub_name']=='Sex and age']


# In[47]:


df_filtered_us.info()


# In[48]:


df_filtered_us.loc[df_filtered_us['stub_label_num'] == 3.110, 'gender'] = 'Male'
df_filtered_us.loc[df_filtered_us['stub_label_num'] == 3.121, 'gender'] = 'Male'
df_filtered_us.loc[df_filtered_us['stub_label_num'] == 3.122, 'gender'] = 'Male'
df_filtered_us.loc[df_filtered_us['stub_label_num'] == 3.131, 'gender'] = 'Male'
df_filtered_us.loc[df_filtered_us['stub_label_num'] == 3.132, 'gender'] = 'Male'
df_filtered_us.loc[df_filtered_us['stub_label_num'] == 3.141, 'gender'] = 'Male'
df_filtered_us.loc[df_filtered_us['stub_label_num'] == 3.142, 'gender'] = 'Male'
df_filtered_us.loc[df_filtered_us['stub_label_num'] == 3.151, 'gender'] = 'Male'
df_filtered_us.loc[df_filtered_us['stub_label_num'] == 3.152, 'gender'] = 'Male'
df_filtered_us.loc[df_filtered_us['stub_label_num'] == 3.153, 'gender'] = 'Male'


# In[49]:


df_filtered_us.loc[df_filtered_us['stub_label_num'] == 3.210, 'gender'] = 'Female'
df_filtered_us.loc[df_filtered_us['stub_label_num'] == 3.221, 'gender'] = 'Female'
df_filtered_us.loc[df_filtered_us['stub_label_num'] == 3.222, 'gender'] = 'Female'
df_filtered_us.loc[df_filtered_us['stub_label_num'] == 3.231, 'gender'] = 'Female'
df_filtered_us.loc[df_filtered_us['stub_label_num'] == 3.232, 'gender'] = 'Female'
df_filtered_us.loc[df_filtered_us['stub_label_num'] == 3.241, 'gender'] = 'Female'
df_filtered_us.loc[df_filtered_us['stub_label_num'] == 3.242, 'gender'] = 'Female'
df_filtered_us.loc[df_filtered_us['stub_label_num'] == 3.251, 'gender'] = 'Female'
df_filtered_us.loc[df_filtered_us['stub_label_num'] == 3.252, 'gender'] = 'Female'
df_filtered_us.loc[df_filtered_us['stub_label_num'] == 3.253, 'gender'] = 'Female'


# In[50]:


df_filtered_us1 = df_filtered_us[(df_filtered_us['gender']=='Male')|(df_filtered_us['gender']=='Female')]


# In[51]:


df_compare1 = df_compare[(df_compare['treatment']=="Yes")&(df_compare['year']==2014)]


# In[52]:


df_compare1.loc[(df_compare1['Age'] <= 14) & (df_compare1['Age'] >= 10), 'age_group'] = "10-14 years"
df_compare1.loc[(df_compare1['Age'] <= 19) & (df_compare1['Age'] >= 15), 'age_group'] = "15-19 years"
df_compare1.loc[(df_compare1['Age'] <= 24) & (df_compare1['Age'] >= 20), 'age_group'] = "20-24 years"
df_compare1.loc[(df_compare1['Age'] <= 34) & (df_compare1['Age'] >= 25), 'age_group'] = "25-34 years"
df_compare1.loc[(df_compare1['Age'] <= 44) & (df_compare1['Age'] >= 35), 'age_group'] = "35-44 years"
df_compare1.loc[(df_compare1['Age'] <= 54) & (df_compare1['Age'] >= 45), 'age_group'] = "45-54 years"
df_compare1.loc[(df_compare1['Age'] <= 64) & (df_compare1['Age'] >= 55), 'age_group'] = "55-64 years"
df_compare1.loc[(df_compare1['Age'] <= 74) & (df_compare1['Age'] >= 65), 'age_group'] = "65-74 years"
df_compare1.loc[(df_compare1['Age'] <= 84) & (df_compare1['Age'] >= 75), 'age_group'] = "75-84 years"
df_compare1.loc[(df_compare1['Age'] >= 85), 'age_group'] = "85 years and over"


# In[53]:


df_plot = pd.DataFrame()
df_plot['value'] = df_compare1[['Gender', 'age_group']].value_counts()


# In[54]:


k = df_plot.reset_index()


# In[55]:


z = k.sort_values(by=['age_group'])


# In[56]:


fig = px.line(z, x='age_group', y='value', color='Gender')
fig.update_xaxes(categoryorder='array', categoryarray= ['15-19 years', '20-24 years', '25-34 years', '35-44 years', '45-54 years', '55-64 years'])

fig.show()
st.plotly_chart(fig, use_container_width=True)


# In[57]:


fig = px.line(df_filtered_us1, x='age', y='estimate', color='gender')
fig.show()
st.plotly_chart(fig, use_container_width=True)


# In[58]:


k = pd.DataFrame()


# In[59]:


k2 = df_compare[df_compare['treatment']=='Yes']


# In[60]:


df_compare.columns


# In[61]:


k['values'] = k2[['Country', 'latitude', 'longitude']].value_counts()


# In[62]:


k3 = k.reset_index()


# In[63]:


m = folium.Map(location = [k3['latitude'].mean(),k3['longitude'].mean()], zoom_start=2, control_scale=True)


# In[64]:


for index, location_info in k3.iterrows():
    folium.CircleMarker([location_info["latitude"], location_info["longitude"]], popup=location_info[['Country', 'values']], radius=location_info['values']/10).add_to(m)


# In[65]:


m


# In[ ]:




