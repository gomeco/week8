#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd
import folium
import numpy as np
import seaborn as sns
import seaborn as sns
import io
import streamlit as st
from streamlit_folium import folium_static
import geopandas as gpd



# In[2]:


st.set_option('deprecation.showPyplotGlobalUse', False)


# In[3]:


#pip install streamlit_folium


# In[4]:


#pip install geopandas


# In[5]:


#pip install plotly


# In[6]:


df=pd.read_csv("survey.csv")


# In[7]:


#df["comments"].unique()


# In[8]:


#df["work_interfere"].unique()


# In[9]:


#df["leave"].unique()


# In[10]:


#df.Age.agg(['min','max'])


# # Data cleanen

# In[11]:


drop_neg = df.drop(df[df['Age'] <18].index, inplace=True)
drop_pos = df.drop(df[df['Age'] > 65].index, inplace=True)


# #Kolom gender cleanen hieronder

# In[12]:


df1=df.replace(dict.fromkeys(['M','male','Male-ish','maile', 'something kinda male?', 
                          'Mal', 'Male (CIS)', 'Make', 'Guy (-ish) ^_^', 'male leaning androgynous',
                          'msle', 'Mail', 'cis male', 'Malr', 'Cis Man', 
                          'ostensibly male', 'm', 'Cis Male', 'Male ', 'Man', 'ostensibly male, unsure what that really means'], 'Male'))
#df1.head(5)


# In[13]:


df2=df1.replace(dict.fromkeys(['female','f', 'F', 'Woman', 'queer/she/they', 'Femake', 'woman', 
                          'Female ', 'cis-female/femme', 'Female (cis)', 'femail', 'Cis Female'], 'Female'))
#df2


# In[14]:


df3= df2.replace(dict.fromkeys(['Trans-female', 'Trans woman', 'Female (trans)', 'non-binary', 
                          'Neuter', 'unsure what that really means', 'queer', 'Genderqueer', 
                          'Androgyne', 'fluid', 'Enby','Nah', 'Agender'], 'Other'))

#df3.head()


# In[15]:


df4=df3.replace(dict.fromkeys(['More than 1000'], np.random.randint(1000,10000,281)))
df5=df4.replace(dict.fromkeys(['500-1000'], np.random.randint(500,1000,59)))
df6=df5.replace(dict.fromkeys(['100-500'], np.random.randint(100,500,175)))
df7=df6.replace(dict.fromkeys(['26-100'], np.random.randint(26,100,288)))
df8=df7.replace(dict.fromkeys(['6-25'], np.random.randint(6,25,289)))
df9=df8.replace(dict.fromkeys(['1-5'], np.random.randint(1,5,158)))


df9['no_employees'].value_counts()


# In[16]:


#df4=df3.replace(dict.fromkeys(['More than 1000'], 5000))
#df5=df4.replace(dict.fromkeys(['500-1000'], 1000))
#df6=df5.replace(dict.fromkeys(['100-500'], 500))
#df7=df6.replace(dict.fromkeys(['26-100'], 100))
#df8=df7.replace(dict.fromkeys(['6-25'], 25))
#df9=df8.replace(dict.fromkeys(['1-5'], 5))


#df9['no_employees'].value_counts()


# In[ ]:





# In[17]:


df9["work_interfere"]=df9["work_interfere"].fillna("Sometimes")


# In[18]:


df9["self_employed"]=df9["self_employed"].fillna("Sometimes")


# In[19]:


#df9 = df9.drop(['Timestamp'], axis = 1)


# In[20]:


df9 = df9.drop(['comments'], axis = 1)


# # Data inspectie

# In[21]:


treatment_gender1=df3.loc[(df3['treatment'] == "Yes") & (df3['Gender'] == "Male")]
#treatment_gender1


procent_m=450*100/990
roundedNumber1 = round(procent_m, 2)

t1 = ("In totaal hebben " + str(roundedNumber1) + 
      " % van de mannen hulp gezocht voor een mentale aandoening binnen een IT bedrijf")

st.write(t1)


# In[22]:


treatment_gender2=df3.loc[(df3['treatment'] == "Yes") & (df3['Gender'] == "Female")]
#treatment_gender2

procent_f=170*100/247
roundedNumber2 = round(procent_f, 2)

t2 = ("In totaal hebben " + str(roundedNumber2) + 
      " % van de vrouwen hulp gezocht voor een mentale aandoening binnen een IT bedrijf")

st.write(t2)


# In[23]:


treatment_gender3=df3.loc[(df3['treatment'] == "Yes") & (df3['Gender'] == "Other")]
#treatment_gender3

procent_o=11*100/13
roundedNumber3 = round(procent_o, 2)

t3 = ("In totaal hebben " + str(roundedNumber3) + 
      " % van Other (geslacht) hulp gezocht voor een mentale aandoening binnen een IT bedrijf")

st.write(t3)


# In[24]:


#df3["Country"].value_counts()


# In[25]:


country_filter=df9.groupby('Country').filter(lambda x : len(x)>=10)


# In[26]:


#Stap 1: Inspecteren in welke landen de meeste werknemers mentale hulp zoeken

treatment_country=country_filter.loc[(country_filter['treatment'] == "Yes")]


# # Outliers verwijderen no_employees

# In[27]:


#outliers verwijderen
st.title('Outliers verwijderen')
country_filter["no_employees"].hist()
st.pyplot()


# In[28]:


# Boxplot functie maken om outlier te zien:

def boxplot(df, ft):
    df.boxplot(column = [ft])
    plt.grid(False)
    plt.show()


# In[29]:


boxplot(country_filter, "no_employees")
st.pyplot()


# In[30]:


#Outlier verwijderen:

#stap 1: alle outliers extraheren 
#stap 2: indexen van ourliers pakken en die verwijderen uit df


def outliers(df, ft):
    Q1 = df[ft].quantile(0.25)
    Q3 = df[ft].quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    ls = df.index[(df[ft] < lower_bound) | (df[ft] > upper_bound)]
    
    return ls
    
    


# In[31]:


#lege lijst maken voor opslaan output indexen 


index_list = []
for employees in ["no_employees"]:
    index_list.extend(outliers(country_filter, employees))


# In[32]:


# verwijderen outliers

def remove(df, ls):
    ls = sorted(set(ls))
    df = df.drop(ls)
    return df


# In[33]:


employees_cleaned = remove(country_filter, index_list)


# In[34]:


boxplot(employees_cleaned, "no_employees")
st.pyplot()


# # Slider met boxplot en scatter

# In[35]:


st.title('Box- en Scatterplots')


# In[ ]:


# Slider met boxplot

fig = px.box(  data_frame=country_filter,  x='treatment',   y='Age',  color='Gender', 
                 animation_frame='Country'
                 
                  ,
            labels={"no_employees": "Aantal werknemers in bedrijf",
                     "treatment": "Hulp zoekend voor mentale aandoening (Y/N)",
                     "Country": "Land",
                    "Gender": "Geslacht",
                 },
                title="Geslachten hulpzoekend mentale problemen gebaseerd op leeftijd")
fig['layout'].pop('updatemenus')
fig.show()
st.plotly_chart(fig, use_container_width=True)


# In[ ]:


# Slider met boxplot

fig = px.scatter(  data_frame=employees_cleaned,  x='no_employees',   y='Age',  color='treatment', 
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


# In[ ]:


employees_cleaned['Timestamp'] = pd.to_datetime(employees_cleaned['Timestamp'], format= '%Y-%m-%d')


# In[ ]:


# Slider met box

fig = px.box(  data_frame=country_filter,  x='Gender',   y='no_employees',  color='leave', 
                 animation_frame='Country'
                 
                  ,
            labels={"leave": "Moeilijkheid vertrekken",
                     "no_employees": "Aantal werknemers",
                     "Country": "Land",
                    "Gender": "Geslacht",
                 },
                title="Moeilijkheid om te vertrekken per geslacht, land en aantal werknemers ")
fig['layout'].pop('updatemenus')
fig.show()
st.plotly_chart(fig, use_container_width=True)


# # Histogrammen

# In[ ]:


st.title('Histogrammen')
px.histogram(df9, x = 'Age' , color = 'treatment' ,
             
             labels={"Age": "Leeftijd",
                     "treatment": "Zoekt hulp",
                     "count": "Aantallen (werknemers)",
                    "Gender": "Geslacht",
                 },
                title="Hoeveel werknemers hulpzoeken, gebaseerd op leeftijd ")
st.pyplot()


# In[ ]:


#Hoevaak geslacht voorkomt
fig = px.histogram(x=df9['Gender'])

fig.update_layout(title='Hoevaak een gender voorkomt in Tech bedrijf')
fig.update_xaxes(title='Geslacht')
fig.update_yaxes(title='Hoeveelheid')

fig.show()
st.plotly_chart(fig, use_container_width=True)


# In[ ]:


#Hoevaak geslacht voorkomt
fig = px.histogram(x=df9['family_history'])

fig.update_layout(title='Hoevaak een mentale aandoening in de familie voorkomt bij werknemers')
fig.update_xaxes(title='Mentale aandoening in de familie (Ja/Nee)')
fig.update_yaxes(title='Hoeveelheid')

fig.show()
st.plotly_chart(fig, use_container_width=True)


# # Boxplots

# In[ ]:


fig = px.box(df9, x="Gender", y="Age", color="treatment",
            labels={"Age": "Leeftijd",
                     "treatment": "Zoekt hulp",
                     "count": "Aantallen (werknemers)",
                    "Gender": "Geslacht",
                 },
                
                title="Hulpzoekend voor mentale aandoening per geslacht")
            



fig.show()
st.plotly_chart(fig, use_container_width=True)


# # NIEUWE DATASET

# In[ ]:


st.title('Hulpbronnen')


# In[ ]:


code1 = '''
df_countries = pd.read_csv('https://raw.githubusercontent.com/gomeco/week8/main/countries.csv')
df_compare = df9.merge(df_countries, left_on = "Country", right_on = "name")
            '''
st.code(code1, language='python')


# In[ ]:


df_countries = pd.read_csv('https://raw.githubusercontent.com/gomeco/week8/main/countries.csv')


# In[ ]:


df_compare = df9.merge(df_countries, left_on = "Country", right_on = "name")


# In[ ]:


df_compare['Timestamp'] = pd.to_datetime(df_compare['Timestamp'])


# In[ ]:


df_compare['year'] = df_compare['Timestamp'].dt.year


# In[ ]:


gdf = gpd.GeoDataFrame(
    df_compare, geometry=gpd.points_from_xy(x=df_compare.longitude, y=df_compare.latitude, crs="EPSG:4326"))


# # Kaart maken

# In[ ]:


st.title('Kaart')


# In[ ]:


def add_categorical_legend(folium_map, title, colors, labels):
    if len(colors) != len(labels):
        raise ValueError("colors and labels must have the same length.")

    color_by_label = dict(zip(labels, colors))
    
    legend_categories = ""     
    for label, color in color_by_label.items():
        legend_categories += f"<li><span style='background:{color}'></span>{label}</li>"
        
    legend_html = f"""
    <div id='maplegend' class='maplegend'>
      <div class='legend-title'>{title}</div>
      <div class='legend-scale'>
        <ul class='legend-labels'>
        {legend_categories}
        </ul>
      </div>
    </div>
    """
    script = f"""
        <script type="text/javascript">
        var oneTimeExecution = (function() {{
                    var executed = false;
                    return function() {{
                        if (!executed) {{
                             var checkExist = setInterval(function() {{
                                       if ((document.getElementsByClassName('leaflet-top leaflet-right').length) || (!executed)) {{
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].style.display = "flex"
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].style.flexDirection = "column"
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].innerHTML += `{legend_html}`;
                                          clearInterval(checkExist);
                                          executed = true;
                                       }}
                                    }}, 100);
                        }}
                    }};
                }})();
        oneTimeExecution()
        </script>
      """
   

    css = """

    <style type='text/css'>
      .maplegend {
        z-index:9999;
        float:right;
        background-color: rgba(255, 255, 255, 1);
        border-radius: 5px;
        border: 2px solid #bbb;
        padding: 10px;
        font-size:12px;
        positon: relative;
      }
      .maplegend .legend-title {
        text-align: left;
        margin-bottom: 5px;
        font-weight: bold;
        font-size: 90%;
        }
      .maplegend .legend-scale ul {
        margin: 0;
        margin-bottom: 5px;
        padding: 0;
        float: left;
        list-style: none;
        }
      .maplegend .legend-scale ul li {
        font-size: 80%;
        list-style: none;
        margin-left: 0;
        line-height: 18px;
        margin-bottom: 2px;
        }
      .maplegend ul.legend-labels li span {
        display: block;
        float: left;
        height: 16px;
        width: 30px;
        margin-right: 5px;
        margin-left: 0;
        border: 0px solid #ccc;
        }
      .maplegend .legend-source {
        font-size: 80%;
        color: #777;
        clear: both;
        }
      .maplegend a {
        color: #777;
        }
    </style>
    """

    folium_map.get_root().header.add_child(folium.Element(script + css))

    return folium_map


# In[ ]:


def color_producer(type):

    if type >300:
        return 'red'
    if (type >200) & (type<300):
        return 'brown'
    if (type >100) & (type<200):
        return 'orange'
    if (type >50) & (type<100):
        return 'yellow'
    if (type >=0) & (type<50):
        return 'green'



# In[ ]:


# punten toevoegen aan map
k = pd.DataFrame()
k2 = df_compare[df_compare['treatment']=='Yes']



k['values'] = k2[['Country', 'latitude', 'longitude']].value_counts()
k3 = k.reset_index()



# In[ ]:


m = folium.Map(location = [k3['latitude'].mean(),k3['longitude'].mean()], zoom_start=2, control_scale=True)



for index, location_info in k3.iterrows():
    color= color_producer(k3['values'].iloc[index])
    folium.CircleMarker([location_info["latitude"], location_info["longitude"]], popup=location_info[['Country', 'values']], radius=location_info['values']/10, color=color).add_to(m)



folium_static(m)


# In[ ]:


#countries_polygonen = geopandas.read_file('countries.geojson')


# # Suicide dataset API

# In[ ]:


code = '''
import http.client
import pandas as pd
conn = http.client.HTTPSConnection("data.cdc.gov")

headers = {}

conn.request("GET", "/resource/9j2v-jamp.csv?$$app_token=uNOBCZDlRBo1hcMQEtpOiMcGm&$limit=999999", headers=headers)

res = conn.getresponse()
data = res.read()
            '''
st.code(code, language='python')


# In[ ]:


import http.client
import pandas as pd
conn = http.client.HTTPSConnection("data.cdc.gov")

headers = {}

conn.request("GET", "/resource/9j2v-jamp.csv?$$app_token=uNOBCZDlRBo1hcMQEtpOiMcGm&$limit=999999", headers=headers)
#token: WxRl58VIg5ybQ2cyCdTHcaUjE
res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))


# In[ ]:


df_suicide_us = pd.read_csv(io.StringIO(data.decode("utf-8")), low_memory=False)


# In[ ]:


df_suicide_us['year'].unique()


# In[ ]:


df_suicide_us_2014 = df_suicide_us[df_suicide_us['year']==2014]


# In[ ]:


df_suicide_us['stub_name'].unique()


# In[ ]:


df_filtered_us = df_suicide_us_2014[df_suicide_us_2014['stub_name']=='Sex and age']


# In[ ]:


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


# In[ ]:


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


# In[ ]:


df_filtered_us1 = df_filtered_us[(df_filtered_us['gender']=='Male')|(df_filtered_us['gender']=='Female')]


# In[ ]:


df_compare1 = df_compare[(df_compare['treatment']=="Yes")&(df_compare['year']==2014)]


# In[ ]:


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


# In[ ]:


df_plot = pd.DataFrame()
df_plot['value'] = df_compare1[['Gender', 'age_group']].value_counts()


# In[ ]:


k = df_plot.reset_index()


# In[ ]:


z = k.sort_values(by=['age_group'])


# In[ ]:


fig = px.line(z, x='age_group', y='value', color='Gender')
fig.update_xaxes(categoryorder='array', 
                 categoryarray= ['15-19 years', '20-24 years', '25-34 years', '35-44 years', '45-54 years', '55-64 years'])

fig.show()
st.plotly_chart(fig, use_container_width=True)


# In[ ]:


fig = px.line(df_filtered_us1, x='age', y='estimate', color='gender',
                labels={"age": "Leeftijd",
                     "estimate": "Aantal zelfmoorden p. 100.000 ",
                     "count": "Aantallen (werknemers)",
                    "gender": "Geslacht",
                 },
                title="Aantal zelfmoorden per geslacht, gebaseerd op leeftijd ")
fig.show()
st.plotly_chart(fig, use_container_width=True)


# In[ ]:


import plotly.express as px

fig = px.scatter(df_filtered_us1, x='age_num', y="estimate", color = 'age',
                 labels={
                     "age_num": "Leeftijdscategorie (1-6)",
                     "estimate": "Zelfmoorden per 100.000 inwoners",
                     "age": "Leeftijd legenda"
                 },
                 title="Aantal zelfmoorden (p 100.000 inwoners) per leeftijdscategorie")
    
fig.show()


st.plotly_chart(fig, use_container_width=True)


# # Voorspellende analyse

# In[ ]:


fig = plt.figure()
sns.regplot(data= df_filtered_us1, x='age_num', y='estimate', ci=None)
sns.scatterplot(data= df_filtered_us1, x='age_num', y='estimate', color = 'red', markers='s')
plt.title('Regressiemodel: Aantal zelfmoorden (p 100.000 inwoners) per leeftijdscategorie')
plt.xlabel('Leeftijdscategorie (1-6)')
plt.ylabel('Aantal zelfmoorden (p 100.000 inwoners)')

fig.show()
st.pyplot(fig)


# In[ ]:


df2 = df_filtered_us1[['age_num', 'estimate']]


# In[ ]:


df2=pd.DataFrame(df2)


# In[ ]:


from sklearn.linear_model import LinearRegression #voor de lineaire regressie
from sklearn.model_selection import train_test_split #voor train en testdata


# In[ ]:


#in train wil ik het aantal niet weergeven, maar in test wel
train = df2.drop(['estimate'], axis=1)
test = df2['estimate']


# In[ ]:


#data splitsen in train en test set
X_train, X_test, y_train, y_test = train_test_split(train, test, test_size=0.3, random_state=2)


# In[ ]:


regr= LinearRegression()


# In[ ]:


regr.fit(X_train, y_train)


# In[ ]:


pred=regr.predict(X_test)


# In[ ]:


pred


# In[ ]:


regr.score(X_test, y_test)


# In[ ]:


fig = plt.figure()

sns.regplot(x=X_test,
            y=y_test,
            data=df2,
            ci=None)


# Show the layered plot
plt.show()
st.pyplot(fig)


# In[ ]:


suicide_voorspelling = pd.DataFrame()


# In[ ]:


suicide_count = df_suicide_us['year'].value_counts()


# In[ ]:


suicide_voorspelling['Aantal zelfmoorden'] = suicide_count


# In[ ]:


suicide_voorspelling = suicide_voorspelling.reset_index()


# In[ ]:


suicide_voorspelling


# In[ ]:


import statsmodels.api as sm


# In[ ]:


X = suicide_voorspelling['index']
Y = suicide_voorspelling['Aantal zelfmoorden']


# In[ ]:


model = sm.OLS(Y, X).fit()
predictions = model.predict(X)

st.write(model.summary())


# In[ ]:




