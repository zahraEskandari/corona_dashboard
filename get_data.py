# -*- coding: utf-8 -*-

# storing and anaysis
import numpy as np
import pandas as pd

# visualization
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
#import folium


#url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'
url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
confirmed_series = pd.read_csv(url, error_bad_lines=False)
#url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv'
url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
Death_series = pd.read_csv(url, error_bad_lines=False)
#url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv'
url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'
Recovered_series = pd.read_csv(url, error_bad_lines=False)



def add_row(df, row):
    df.loc[-1] = row
    df.index = df.index + 1  
    return df.sort_index()




confirmed_df = pd.DataFrame(columns=('Province/State','Country/Region' , 'Lat' , 'Long' , 'Date', 'Confirmed'))
for index, row in confirmed_series.iterrows():
    row = row.tolist()
    r1 = row[0:4]
    for i in range(4 , len(row)):
        r2 = r1 + [ confirmed_series.columns[i], row[i] ]
        add_row(confirmed_df, r2) 




Death_df = pd.DataFrame(columns=('Province/State','Country/Region' , 'Lat' , 'Long' , 'Date', 'Deaths'))
for index, row in Death_series.iterrows():
    row = row.tolist()
    r1 = row[0:4]
    for i in range(4 , len(row)):
        r2 = r1 + [ Death_series.columns[i], row[i] ]
        add_row(Death_df, r2) 
        
  
Death_df.head()




Recovered_df = pd.DataFrame(columns=('Province/State','Country/Region' , 'Lat' , 'Long' , 'Date', 'Recovered'))
for index, row in Recovered_series.iterrows():
    row = row.tolist()
    r1 = row[0:4]
    for i in range(4 , len(row)):
        r2 = r1 + [ Recovered_series.columns[i], row[i] ]
        add_row(Recovered_df, r2) 
        
  
Recovered_df.head()

confirmed_df['Date'] = pd.to_datetime(confirmed_df['Date'])
Death_df['Date'] = pd.to_datetime(Death_df['Date'])
Recovered_df['Date'] = pd.to_datetime(Recovered_df['Date'])
c_d_df = pd.merge(confirmed_df, Death_df,  how='left'
                  , left_on=['Province/State','Country/Region' , 'Lat' , 'Long' , 'Date']
                  , right_on = ['Province/State','Country/Region' , 'Lat' , 'Long' , 'Date'])

c_d_df.head()
full_df = pd.merge(c_d_df, Recovered_df,  how='left'
                  , left_on=['Province/State','Country/Region' , 'Lat' , 'Long' , 'Date']
                  , right_on = ['Province/State','Country/Region' , 'Lat' , 'Long' , 'Date'])

full_df['Date']= pd.to_datetime(full_df['Date']) 
full_df.head()


full_df.to_csv('path to ..\\data\\corona_data.csv')


