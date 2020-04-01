#from flask import Flask
import flask
import dash
import dash_core_components as dcc
import dash_html_components as html


import pandas as pd
import plotly.graph_objs as go
import random
import math 
import dash_table as dst
from dash.dependencies import Input, Output
import datetime
import plotly
# storing and anaysis
import numpy as np

# visualization
#import matplotlib.pyplot as plt
#import seaborn as sns
import plotly.express as px
import folium
#from time import  strftime
from flask_caching import Cache
import json

data_path = 'path to .. \\data\\corona_data.csv'

external_scripts = [
    {'src': 'my view counter script'}    
]

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server,  external_scripts=external_scripts)





# show data 
def serve_layout():   
    # importing datasets
   
    full_table = pd.read_csv(data_path , 
                             parse_dates=['Date'])
                             
    # unifying names 
    full_table['Country/Region'] = full_table['Country/Region'].replace('Mainland China', 'China')
    full_table['Country/Region'] = full_table['Country/Region'].replace('Iran (Islamic Republic of)', 'Iran')
    full_table['Country/Region'] = full_table['Country/Region'].replace('Republic of Korea', 'South Korea')
    full_table['Country/Region'] = full_table['Country/Region'].replace('Korea, South', 'South Korea')
    
    # filling missing values with NA
    full_table[['Province/State']] = full_table[['Province/State']].fillna('NA')
    Iran = full_table[full_table['Country/Region']=='Iran']
    full_latest = full_table[full_table['Date'] == max(full_table['Date'])].reset_index()
    
    # last 2 days
    temp = full_table.groupby('Date')['Confirmed', 'Deaths', 'Recovered'].sum()
    temp = temp.reset_index()
    temp = temp.sort_values('Date', ascending=False)

    today = temp.iloc[0]["Date"]
    t = str(today)#today.strftime("%d-%b-%Y") 
    today = t[0:t.find('T')]
    total_cases_today = temp.iloc[0]["Confirmed"]
    death_cases_today = temp.iloc[0]["Deaths"]
    recovered_cases_today = temp.iloc[0]["Recovered"]
    print(temp.head())
    yesterday = temp.iloc[1]["Date"]
    total_cases_yesterday = temp.iloc[1]["Confirmed"]
    death_cases_yesterday = temp.iloc[1]["Deaths"]
    recovered_cases_yesterday = temp.iloc[1]["Recovered"]
    
    temp_Iran = Iran.groupby('Date')['Confirmed', 'Deaths', 'Recovered'].sum()
    temp_Iran = temp_Iran.reset_index()
    temp_Iran = temp_Iran.sort_values('Date', ascending=False)

    iran_today = temp_Iran.iloc[0]["Date"]
    iran_total_cases_today = temp_Iran.iloc[0]["Confirmed"]
    iran_death_cases_today = temp_Iran.iloc[0]["Deaths"]
    iran_recovered_cases_today = temp_Iran.iloc[0]["Recovered"]
    
    iran_yesterday = temp_Iran.iloc[1]["Date"]
    iran_total_cases_yesterday = temp_Iran.iloc[1]["Confirmed"]
    iran_death_cases_yesterday = temp_Iran.iloc[1]["Deaths"]
    iran_recovered_cases_yesterday = temp_Iran.iloc[1]["Recovered"]

    full_latest = full_table[full_table['Date'] == max(full_table['Date'])].reset_index()
    full_latest_grouped = full_latest.groupby('Country/Region')['Confirmed', 'Deaths', 'Recovered'].sum().reset_index()
    full_latest_grouped_confirmed = full_latest_grouped[['Country/Region', 'Confirmed']]
    result =  full_latest_grouped_confirmed.nlargest(8, columns='Confirmed')
    print(int(full_latest_grouped_confirmed.loc[full_latest_grouped_confirmed['Country/Region']=='Iran'] ["Confirmed"]))
    
    if 'Iran' not in result['Country/Region'].values : 
       result.loc[len(result)] = ['Iran', int(full_latest_grouped_confirmed.loc[full_latest_grouped_confirmed['Country/Region']=='Iran'] ["Confirmed"])]
                     
    result.loc[len(result)] = ['Other Countries', full_latest_grouped_confirmed.loc[~full_latest_grouped_confirmed['Country/Region'].isin(result['Country/Region']), 'Confirmed'].sum()]
    #full_latest_grouped_confirmed
    result
         
    temp_full = full_table.groupby(['Country/Region', 'Date'])['Confirmed', 'Deaths', 'Recovered'].sum()
    temp_full = temp_full.reset_index()
    #temp_full['Country/Region'].isin(result['Country/Region'])
    temp = temp_full.loc[temp_full['Country/Region'].isin(result['Country/Region']) ]
    temp2 = temp_full.loc[~temp_full['Country/Region'].isin(result['Country/Region']) ].groupby(['Date'])['Confirmed', 'Deaths', 'Recovered'].sum()
    temp2 = temp2.reset_index()
    temp2['Country/Region'] = 'Other Countries'
    temp = temp.append(temp2, ignore_index=True)
    temp
    
    
    fig1 = px.bar(temp, x="Date", y="Confirmed", color='Country/Region', orientation='v',width= 600 ,  height=600,
                  title='مجموع موارد تایید شده در دنیا', color_discrete_sequence = px.colors.cyclical.HSV)
    fig1.update_layout(legend_orientation='h')    #fig.show()
    
    fig2 = px.bar(temp, x="Date", y="Deaths", color='Country/Region', orientation='v', width= 600 , height=600,
                  title='مجموع موارد فوت شده در دنیا', color_discrete_sequence = px.colors.cyclical.HSV)
    fig2.update_layout(legend_orientation='h')    #fig.show()

    fig3= px.line(temp, x='Date', y='Confirmed', color='Country/Region', width= 600 , height=600, 
                  title=' موارد تایید شده به تفکیک کشور', color_discrete_sequence = px.colors.cyclical.HSV )
    fig3.update_layout(legend_orientation='h')#fig.show()
    
    fig4= px.line(temp, x='Date', y='Deaths', color='Country/Region' , width= 600 , height=600,
                  title=' موارد فوت شده به تفکیک کشور', color_discrete_sequence = px.colors.cyclical.HSV )
    fig4.update_layout(legend_orientation='h')#fig.show()



    gdf = gdf = full_table.groupby(['Date', 'Country/Region'])['Confirmed', 'Deaths', 'Recovered'].max()
    gdf = gdf.reset_index()
    
    
    temp_iran = gdf[gdf['Country/Region']=='Iran'].groupby('Date').sum().reset_index()
    temp_iran = temp_iran.melt(id_vars='Date', value_vars=['Confirmed', 'Deaths', 'Recovered'],
                    var_name='Case', value_name='Count')
    fig5 = px.bar(temp_iran, x="Date", y="Count", color='Case', facet_col="Case",
                  title='مجموع موارد تایید شده، فوت شده و بهبود یافته ایران' , width=1000)
    
    temp_iran2 = Iran.groupby('Date')['Confirmed', 'Deaths', 'Recovered'].sum().diff()
    print(temp_iran2)
    temp_iran2 = temp_iran2.reset_index()
    temp_iran2 = temp_iran2.melt(id_vars="Date", 
             value_vars=['Confirmed', 'Deaths', 'Recovered'])
        
    fig9 = px.bar(temp_iran2, x="Date", y="value", color='variable', 
                     title='تعداد موارد تایید شده، فوت شده و بهبود یافته ایران در هر روز' , width=1000)
    fig9.update_layout(barmode='group')
    
    temp['Mortality Rate'] = round(1.0 * temp['Deaths']/
                                                      temp['Confirmed'], 3)*100
    temp['Recovery Rate'] = round(1.0 * temp['Recovered']/
                                                         temp['Confirmed'], 3)*100
    #fig5.show()
    
    fig6 = px.line(temp, x="Date", y='Mortality Rate', color='Country/Region', 
              facet_col='Country/Region',hover_name='Country/Region' , facet_col_wrap  = 3 , render_mode = 'webgl'
              , title='نرخ موارد منجر به مرگ نسبت به موارد تایید شده در طول زمان' , width=1000 , height=700)
    fig6.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    
    
    fig7 = px.line(temp, x="Date", y='Recovery Rate', color='Country/Region', 
              facet_col='Country/Region',hover_name='Country/Region' , facet_col_wrap  = 3 , render_mode = 'webgl'
              , title='نرخ موارد بهبود یافته نسبت به موارد تایید شده در طول زمان' , width=1000 , height=700)
    fig7.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))


    fig8 = px.line(temp, x="Date", y='Confirmed', color='Country/Region', 
                  facet_col='Country/Region',hover_name='Country/Region' , facet_col_wrap  = 3 , render_mode = 'auto'
                  , title='تعداد موارد تایید شده در کشورهای مختلف' , width=1000 , height=700)
    fig8.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

    
    colors = {
        'background': '#222222',
        'text': '#7FDBFF'
    }


    d1 = html.Div( id = 'd1'  , className = 'class list emergency' , style={'color':'white' , 'border':'solid 1px white' , 'direction':'rtl' , 'padding':'20px' , 'margin':'8px' }
                    , children=[ 
                             html.Div(  className = 'content'
                                             , children=[
                                                      html.Div( className = 'content'  , children =  html.Span( style={'font-size': '24px' } ,children='موارد تایید شده در دنیا'  ))
                                                     ,html.Div(  id ='confirmedCases_count' , style= {'color':'red' , 'font-size': '48px' } , className = 'heading1' , children = "{:,d}".format(int(total_cases_today))  ) #
                                                     ,html.Div( className = 'content'  , children =  "{:,d}".format(int(total_cases_today - total_cases_yesterday))  +  ' مورد بیشتر از روز قبل' ) #"{:,d}".format(total_cases_today - total_cases_yesterday)  +  ' مورد بیشتر از روز قبل' 
                                                     
								              ]
                             )
                            , html.Div(  className = 'metadata' , children='تاریخ به روز رسانی:'  + str(today) ) #'تاریخ به روز رسانی:'  + today.strftime("%b %d %Y") 
                    ]
            )
                             
    d2 = html.Div( id = 'd2'  , className = 'class list emergency' , style={'color':'white' , 'border':'solid 1px white' , 'direction':'rtl' , 'padding':'20px' , 'margin':'8px'}
                    , children=[ 
                             html.Div(  className = 'content'
                                             , children=[
                                                      html.Div( className = 'content'  , children =  html.Span( style={'font-size': '24px' } ,children='موارد فوت شده در دنیا'  ))
                                                     ,html.Div(  id ='DeathsCases_count' , style= {'color':'red' , 'font-size': '48px' } , className = 'heading1' , children = "{:,d}".format(int(death_cases_today))  ) #str(total_cases_today)
                                                     ,html.Div( className = 'content'  , children = "{:,d}".format(int(death_cases_today - death_cases_yesterday) ) +  ' مورد بیشتر از روز قبل'  )
                                                     
								              ]
                             )
                            , html.Div(  className = 'metadata' , children= 'تاریخ به روز رسانی:'  + str(today) )
                    ]
            )
                             
                             
    d3 = html.Div( id = 'd3'  , className = 'class list emergency' , style={'color':'white' , 'border':'solid 1px white' , 'direction':'rtl' , 'padding':'20px' , 'margin':'8px'}
                    , children=[ 
                             html.Div(  className = 'content'
                                             , children=[
                                                      html.Div( className = 'content'  , children =  html.Span( style={'font-size': '24px' } ,children='موارد بهبود یافته در دنیا'  ))
                                                     ,html.Div(  id ='RecoveredCases_count' , style= {'color':'red' , 'font-size': '48px' } , className = 'heading1' , children = "{:,d}".format(int(recovered_cases_today))  ) #str(total_cases_today)
                                                     ,html.Div( className = 'content'  , children = "{:,d}".format(int(recovered_cases_today - recovered_cases_yesterday))  +  ' مورد بیشتر از دیروز'  )
                                                     
								              ]
                             )
                            , html.Div(  className = 'metadata' , children= 'تاریخ به روز رسانی:'  + str(today) )#today.strftime("%b %d %Y")
                    ]
            )
     
                      
    d1_iran = html.Div( id = 'd1_iran'  , className = 'class list emergency'  , style={'color':'white' , 'border':'solid 1px white' , 'direction':'rtl' , 'padding':'20px' , 'margin':'8px' }
                    , children=[ 
                             html.Div(  className = 'content'
                                             , children=[
                                                      html.Div( className = 'content'  , children =  html.Span( style={'font-size': '24px' } ,children='موارد تایید شده در ایران'  ))
                                                     ,html.Div(  id ='iran_confirmedCases_count' , style= {'color':'red' , 'font-size': '48px' } , className = 'heading1' , children = "{:,d}".format( int(iran_total_cases_today))  ) #str(total_cases_today)
                                                     ,html.Div( className = 'content'  , children = "{:,d}".format( int(iran_total_cases_today - iran_total_cases_yesterday))  + ' مورد بیشتر از روز قبل' )
                                                     
								              ]
                             )
                            , html.Div(  className = 'metadata' , children= 'تاریخ به روز رسانی:'  + str(today) )
                    ]
            )
        
                             
    d2_iran = html.Div( id = 'd2_iran'  , className = 'class list emergency' , style={'color':'white' , 'border':'solid 1px white' , 'direction':'rtl' , 'padding':'20px' , 'margin':'8px'}
                    , children=[ 
                             html.Div(  className = 'content'
                                             , children=[
                                                      html.Div( className = 'content'  , children =  html.Span( style={'font-size': '24px' } ,children='موارد فوت شده در ایران'  ))
                                                     ,html.Div(  id ='iran_DeathsCases_count' , style= {'color':'red' , 'font-size': '48px' } , className = 'heading1' , children = "{:,d}".format( int(iran_death_cases_today))  ) #str(total_cases_today)
                                                     ,html.Div( className = 'content'  , children = "{:,d}".format(int(iran_death_cases_today - iran_death_cases_yesterday) ) + ' مورد بیشتر از روز قبل' )
                                                     
								              ]
                             )
                            , html.Div(  className = 'metadata' , children= 'تاریخ به روز رسانی:'  + str(today) )
                    ]
            )
                             
                             
    d3_iran = html.Div( id = 'd3_iran'  , className = 'class list emergency' , style={'color':'white' , 'border':'solid 1px white' , 'direction':'rtl' , 'padding':'20px' , 'margin':'8px'}
                    , children=[ 
                             html.Div(  className = 'content'
                                             , children=[
                                                      html.Div( className = 'content'  , children =  html.Span( style={'font-size': '24px' } ,children='موارد بهبود یافته در ایران'  ))
                                                     ,html.Div(  id ='iran_RecoveredCases_count' , style= {'color':'red' , 'font-size': '48px' } , className = 'heading1' , children = "{:,d}".format(int(iran_recovered_cases_today))  ) #str(total_cases_today)
                                                     ,html.Div( className = 'content'  , children = "{:,d}".format(int(iran_recovered_cases_today - iran_recovered_cases_yesterday))  + ' مورد بیشتر از روز قبل' )
                                                     
								              ]
                             )
                            , html.Div(  className = 'metadata' , children= 'تاریخ به روز رسانی:'  + str(today) )
                    ]
            )
    confirmed_cases_fig_div = html.Div(  style={ 'display': 'flex' , 'flex-direction': 'column' , 'justify-content': 'center' , 'backgroundColor': colors['background']}
                                             , children=[html.Div(  
                                                              style={'display': 'flex' , 'flex-direction': 'row' ,  'margin-left' :'10px', 'margin-right' :'10px'} 
                                                              , children = dcc.Graph( id='life-exp-vs-gdp6', figure = fig1) 
                                                              )
                                                     ]
                                         )
                                             
    confirmed_cases_fig_div_2 = html.Div(  style={ 'display': 'flex' , 'flex-direction': 'column' , 'justify-content': 'center' , 'backgroundColor': colors['background']}
                                             , children=[html.Div(  
                                                              style={'display': 'flex' , 'flex-direction': 'row' ,  'margin-left' :'10px', 'margin-right' :'10px'} 
                                                              , children = dcc.Graph( id='confirmed_cases_fig_div_2', figure = fig3) 
                                                              )
                                                     ]
                                         )
    deaths_cases_fig_div = html.Div(  style={ 'display': 'flex' , 'flex-direction': 'column' , 'justify-content': 'center' , 'backgroundColor': colors['background']}
                                             , children=[ html.Div(  
                                                              style={'display': 'flex' , 'flex-direction': 'row' ,  'margin-left' :'10px', 'margin-right' :'10px'} 
                                                              , children = dcc.Graph( id='life-exp-vs-gdp7', figure = fig2) 
                                                              )
                                                     ]
                                         )
    deaths_cases_fig_div_2 = html.Div(  style={ 'display': 'flex' , 'flex-direction': 'column' , 'justify-content': 'center' , 'backgroundColor': colors['background']}
                                             , children=[ html.Div(  
                                                              style={'display': 'flex' , 'flex-direction': 'row' ,  'margin-left' :'10px', 'margin-right' :'10px'} 
                                                              , children = dcc.Graph( id='deaths_cases_fig_div_2', figure = fig4) 
                                                              )
                                                     ]
                                         )
                                             
    
    iran_status = html.Div(  style={ 'display': 'flex' , 'flex-direction': 'column' , 'justify-content': 'center' , 'backgroundColor': colors['background']}
                                             , children=[ html.Div(  
                                                              style={'display': 'flex' , 'flex-direction': 'row' ,  'margin-left' :'10px', 'margin-right' :'10px'} 
                                                              , children = dcc.Graph( id='iran_status', figure = fig5) 
                                                              )
                                                     ]
                                         )
    iran_daily_status = html.Div(  style={ 'display': 'flex' , 'flex-direction': 'column' , 'justify-content': 'center' , 'backgroundColor': colors['background']}
                                             , children=[ html.Div(  
                                                              style={'display': 'flex' , 'flex-direction': 'row' ,  'margin-left' :'10px', 'margin-right' :'10px'} 
                                                              , children = dcc.Graph( id='iran_daily_status', figure = fig9) 
                                                              )
                                                     ]
                                         )
                                             
    mortality_rate = html.Div(  style={ 'display': 'flex' , 'flex-direction': 'column' , 'justify-content': 'center' , 'backgroundColor': colors['background']}
                                             , children=[ html.Div(  
                                                              style={'display': 'flex' , 'flex-direction': 'row' ,  'margin-left' :'10px', 'margin-right' :'10px'} 
                                                              , children = dcc.Graph( id='mortality_rate', figure = fig6) 
                                                              )
                                                     ]
                                         )                            
                                             
    recovery_rate = html.Div(  style={ 'display': 'flex' , 'flex-direction': 'column' , 'justify-content': 'center' , 'backgroundColor': colors['background']}
                                             , children=[ html.Div(  
                                                              style={'display': 'flex' , 'flex-direction': 'row' ,  'margin-left' :'10px', 'margin-right' :'10px'} 
                                                              , children = dcc.Graph( id='reconvery_rate', figure = fig7) 
                                                              )
                                                     ]
                                         )
                                             
    confirmed_cases_faceted = html.Div(  style={ 'display': 'flex' , 'flex-direction': 'column' , 'justify-content': 'center' , 'backgroundColor': colors['background']}
                                             , children=[ html.Div(  
                                                              style={'display': 'flex' , 'flex-direction': 'row' ,  'margin-left' :'10px', 'margin-right' :'10px'} 
                                                              , children = dcc.Graph( id='confirmed_cases_faceted', figure = fig8) 
                                                              )
                                                     ]
                                         )
                          
                    
    
                             
    
    date_string = f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S%z}'
    return html.Div(   style={ 'display': 'flex' , 'flex-direction': 'column' , 'justify-content': 'center' , 'backgroundColor': colors['background']} 
        ,children=[  
        html.Div(
                children=[ 
                        html.H1(style={'color':'white' , 'text-align':'center'} , children='وضعیت انتشار کرونا در ایران و دنیا')     
                        , html.H5(style={'color':'white' , 'text-align':'center'} , children='Loaded at: ' +date_string) 
                  ]
                ) 
         , html.Div( id="global_stats"  , children = [ d1 , d2 , d3] 
                    , style= { 'display': 'flex' , 'flex-direction': 'row' , 'justify-content': 'center' 
                              ,  'margin-bottom' :'20px' , 'backgroundColor': colors['background'] , 'direction':'rtl'} 
           )
         , html.Div( id="iran_stats"  , children = [ d1_iran , d2_iran , d3_iran] 
                    , style= { 'display': 'flex' , 'flex-direction': 'row' , 'justify-content': 'center' 
                              ,  'margin-bottom' :'30px' , 'backgroundColor': colors['background'] , 'direction':'rtl'} 
           )
         
         
        , html.Div(
                    style={ 'display': 'flex' , 'flex-direction': 'row' , 'justify-content': 'center' ,  'margin-bottom' :'10px' , 'backgroundColor': colors['background'] , 'direction' : 'rtl'} 
                    , children=[ 
                                confirmed_cases_fig_div ,  deaths_cases_fig_div
                            ]
                 )
        , html.Div(
                    style={ 'display': 'flex' , 'flex-direction': 'row' , 'justify-content': 'center' ,  'margin-bottom' :'10px' , 'backgroundColor': colors['background'] , 'direction' : 'rtl'} 
                    , children=[ 
                                confirmed_cases_fig_div_2 ,  deaths_cases_fig_div_2
                            ]
                 )
         , html.Div(
                    style={ 'display': 'flex' , 'flex-direction': 'row' , 'justify-content': 'center' ,  'margin-bottom' :'10px' , 'backgroundColor': colors['background'] , 'direction' : 'rtl'} 
                    , children = iran_status
                 )
           , html.Div(
                    style={ 'display': 'flex' , 'flex-direction': 'row' , 'justify-content': 'center' ,  'margin-bottom' :'10px' , 'backgroundColor': colors['background'] , 'direction' : 'rtl'} 
                    , children = iran_daily_status
                 )
         , html.Div(
                    style={ 'display': 'flex' , 'flex-direction': 'row' , 'justify-content': 'center' ,  'margin-bottom' :'10px' , 'backgroundColor': colors['background'] , 'direction' : 'rtl'} 
                    , children = confirmed_cases_faceted
                 )
         
         , html.Div(
                    style={ 'display': 'flex' , 'flex-direction': 'row' , 'justify-content': 'center' ,  'margin-bottom' :'10px' , 'backgroundColor': colors['background'] , 'direction' : 'rtl'} 
                    , children = mortality_rate
                 )
          , html.Div(
                    style={ 'display': 'flex' , 'flex-direction': 'row' , 'justify-content': 'center' ,  'margin-bottom' :'10px' , 'backgroundColor': colors['background'] , 'direction' : 'rtl'} 
                    , children = recovery_rate
                 )
          
          #, html.A(href="http://www.webgozar.com/counter/stats.aspx?code=3745510" , target="_blank" , children='&#1570;&#1605;&#1575;&#1585;')
          
          , html.Div(
                style={ 'display': 'flex' , 'flex-direction': 'row' , 'justify-content': 'center' ,  'margin-bottom' :'10px' , 'backgroundColor': colors['background'] , 'direction' : 'rtl'} 
                    , children = [
                              html.Span( style= {'color':'white'} , children=' این داشبورد بر اساس داده‌های آماری دانشگاه جان هاپکینز آمریکا تهیه شده است.  از طریق لینک زیر می توانید به این داده ها دسترسی پیدا کنید. ')
                              
                        ]
            )
            , html.Div(
                style={ 'display': 'flex' , 'flex-direction': 'row' , 'justify-content': 'center' ,  'margin-bottom' :'10px' , 'backgroundColor': colors['background'] , 'direction' : 'rtl'} 
                    , children = [
                              
                               html.A(style= {'color':'white'} , href="https://github.com/CSSEGISandData/COVID-19" , target="_blank" , children='https://github.com/CSSEGISandData/COVID-19')
                              ,html.Br()
                        ]
            )
            , html.Div(
                style={ 'display': 'flex' , 'flex-direction': 'row' , 'justify-content': 'center' ,  'margin-bottom' :'10px' , 'backgroundColor': colors['background'] , 'direction' : 'rtl'} 
                    , children = [
                              html.Span( style= {'color':'white'} , children='برای ارتباط با من می توانید روی وبلاگ دیتا اینسایتز به آدرس زیر پیام بگذارید :   ')
                              #, html.A(style= {'color':'white'} , href="https://datainsights.blogsky.com/" , target="_blank" , children=' دیتا اینسایتز ')                             
                              
                        ]
            )
            , html.Div(
                style={ 'display': 'flex' , 'flex-direction': 'row' , 'justify-content': 'center' ,  'margin-bottom' :'10px' , 'backgroundColor': colors['background'] , 'direction' : 'rtl'} 
                    , children = [
                             
                              html.A(style= {'color':'white'} , href="https://datainsights.blogsky.com/" , target="_blank" , children='https://datainsights.blogsky.com/ ')                             
                              
                        ]
            )
           
        
         
         
           
    ])
              
app.layout = serve_layout
app.scripts.append_script({"external_url": "http://www.webgozar.ir/c.aspx?Code=3570732&amp;t=counter"})


          
if __name__ == '__main__':
    #app.run_server(debug=True)
    app.run_server(debug=False , dev_tools_hot_reload=False)