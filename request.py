import requests
import json
import numpy as np
import pandas as pd
import dash_core_components as dcc
import dash
import dash_html_components as html
from bs4 import BeautifulSoup
import contentlinks as content

def loadContent(url,clink,hlink,tlink, ilink,https):
    response = requests.get(url)
    if response.status_code == 200:
        titles = []
        links = []
        imgurls = []
        content = response.content
        number_of_articles = 10
        soup1 = BeautifulSoup(content, features="html.parser")
        coverpage_news = soup1.find_all(class_=clink)
        for n in np.arange(0, number_of_articles):
            link = coverpage_news[n].find('a', class_=hlink)['href']
            title = coverpage_news[n].find(span, class_=tlink).get_text()
            imgurl = coverpage_news[n].find(class_=ilink)['src']
            link = ''.join((https, link))
            links.append(link)
            imgurls.append(imgurl)
            titles.append(title)
            table = {'IMG' : imgurls, 'TITLE' :titles, 'LINK' : links}
        return table
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
    return html.Table( children=
        [html.Tr([html.Th(col) for col in dataframe.columns])] + rows,
        className='newstable',
    )

def append_content(app, data):
    df = establishDataframe(data)
    app.layout = html.Div(children=[
        html.H1(children='Headlines'),
        generate_table(df)
    ])
    return app

def generateWebServer():
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    for n in range(len(content.websiteUrl)):
        data = loadContent(content.websiteUrl[n],
        content.websiteclasslink[n],
        content.websiteHLink[n],
        content.websiteTitle[n],
        content.websiteImage[n],
        content.websiteHTTP[n])

        append_content(app, data)

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