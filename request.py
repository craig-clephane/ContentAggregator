import requests
import json
import numpy as np
import pandas as pd
import dash_core_components as dcc
import dash
import dash_html_components as html
from bs4 import BeautifulSoup
import contentlinks as content

titles = []
links = []
imgurls = []

def loadContent(url,clink,hlink,tlink, ilink,https):
    response = requests.get(url)
    if response.status_code == 200:
        content = response.content
        soup1 = BeautifulSoup(content, features="html.parser")
        coverpage_news = soup1.find_all(class_=clink)
        number_of_articles = 20
        for n in np.arange(0, number_of_articles):
            link = coverpage_news[n].find('a', class_=hlink)['href']
            title = coverpage_news[n].find('span', class_=tlink).get_text()
            imgurl = coverpage_news[n].find(class_=ilink)['src']
            link = ''.join((https, link))
            links.append(link)
            imgurls.append(imgurl)
            titles.append(title)
    elif response.status_code == 404:
        print("Website not found")
        return

def generate_table(dataframe):
    rows = []
    for i in range(len(dataframe)):
        row = []
        for col in dataframe.columns:
            value = dataframe.iloc[i][col]
            if col == 'IMG':
                cell = html.Td(html.Img(src=value, height='20%'))
            if col == 'TITLE':
                cell = html.Td(children=value)
            if col == 'LINK':
                cell = html.Td(html.A(href=value, children=value))
            row.append(cell)
        rows.append(html.Tr(row))
    return html.Table(
        [html.Tr([html.Th(col) for col in dataframe.columns])] + rows
    )

def generateWebServer(sel):
    if sel == "YES":
        external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
        app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
        app.layout = html.Div(children=[
            html.H1(children='News Headlines'),
            generate_table(df)
        ])
        app.run_server()
    else:
        return

for n in range(len(content.websiteUrl)):
    loadContent(content.websiteUrl[n],
    content.websiteclasslink[n],
    content.websiteHLink[n],
    content.websiteTitle[n],
    content.websiteImage[n],
    content.websiteHTTP[n]
    )
    table = {'IMG' : imgurls, 'TITLE' :titles, 'LINK' : links}
    df = pd.DataFrame(table)

    generateWebServer(input("Load Web Server?").upper())