import establishConntection as connection
from bs4 import BeautifulSoup
import requests
import numpy as np

url = 'https://news.sky.com/'
titleAndLink = []
imgurls = []
number_of_articles = 10

def skynewsContent():
    response = requests.get(url)
    if connection.status_code(response):
        content = response.content
        soup1 = BeautifulSoup(content, features="html.parser")
        coverpage_news = soup1.find_all(class_='sdc-site-tiles__item sdc-site-tile sdc-site-tile--has-link')
        for n in np.arange(0, number_of_articles):
            link = coverpage_news[n].find('a', class_="sdc-site-tile__headline-link")['href']
            title = coverpage_news[n].find('span', class_="sdc-site-tile__headline-text").get_text()
            #imgurl = coverpage_news[n].find(class_="sdc-site-tile__image")['src']
            link = ''.join((url, link))
            titleAndLink.append([title, link])
            #imgurls.append(imgurl)
            #table = {'IMG' : imgurls, 'TITLE' :titles, 'LINK' : links}
            #table = {'TITLE' :titles, 'LINK' : links}
        return titleAndLink
    elif response.status_code == 404:
        print("Website not found")
        return