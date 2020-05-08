import json
import numpy as np
import pandas as pd
import dash_core_components as dcc
import dash
import dash_html_components as html
from bs4 import BeautifulSoup
import skynews as skynews
import bbcnews as bbcnews
import grimsbytelegraph as grimsby
import verge as verge

def generate_table(dataframe):
    rows = []
    for i in range(len(dataframe)):
        row = []
        value = dataframe.iloc[i][:]
            # if col == 'IMG':
            #     cell = html.Td(html.Img(src=value, height='20%'))
            # if col == 'TITLE':
            #     cell = html.Td(children=value)
            # if col == 'LINK':
            #     cell = html.Td(html.A(href=value, children=value))
        cell = html.Td(html.A(href=value[1], children=value[0], className='article_title'))
        row.append(cell)
        rows.append(html.Tr(row, className='contentRow'))
    return html.Table( children=
        [html.Tr(rows)],
        className='newstable'
    )

def append_content(app):
   
    app.layout = html.Div(className='table', 
    children=[
        ##html.H1(children='Headlines'),
        html.Div(className='content', children=[
            html.H6(children='BBC'),
            generate_table(establishDataframe(bbcnews.bbcnewscontent()))
        ]),
        html.Div(className='content', children=[
            html.H6(children='Sky'),
            generate_table(establishDataframe(skynews.skynewsContent()))
        ]),
        html.Div(className='content', children=[
            html.H6(children='GrimsbyTelegraph'),
            generate_table(establishDataframe(grimsby.grimsbytelegraphContent()))
        ]),
        html.Div(className='content', children=[
            html.H6(children='Verge'),
            generate_table(establishDataframe(verge.vergeContent()))
        ])  
    ])
    html.Div(className='table', 
    children=[
        html.H1(children='Headlines'),  
    ])
    return app

def generateWebServer():
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'
    ]
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    append_content(app)
    
    runWebServer(app, input("Load Web Server?").upper())
    
def establishDataframe(table):
    df = pd.DataFrame(table)
    return df

def runWebServer(app, sel):
    if sel == "YES":
        app.run_server()
    else:
        return    

generateWebServer()