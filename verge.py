import establishConntection as connection
from bs4 import BeautifulSoup
import requests
import numpy as np

url = 'https://www.theverge.com/'
titles = []
links = []
imgurls = []
number_of_articles = 10

def vergeContent():
    response = requests.get(url)
    if connection.status_code(response):
        content = response.content
        soup1 = BeautifulSoup(content, features="html.parser")
        coverpage_news = soup1.find_all(class_='c-entry-box--compact c-entry-box--compact--article')
        for n in np.arange(0, number_of_articles):
            ##print(coverpage_news[n])
            link = coverpage_news[n].find('h2', class_="c-entry-box--compact__title")
            link = link.find('a')['href']
            title = coverpage_news[n].find('h2', class_="c-entry-box--compact__title")
            title = title.find('a').get_text()
            #imgurl = coverpage_news[n].find(class_="sdc-site-tile__image")['src']
            if link[:4] != 'http':
                link = ''.join(('https://www.theverge.com/', link))
            else:
                print("link correct")
            links.append(link)
            #imgurls.append(imgurl)
            titles.append(title)
            #table = {'IMG' : imgurls, 'TITLE' :titles, 'LINK' : links}
            table = {'TITLE' :titles, 'LINK' : links}
        return table
    elif response.status_code == 404:
        print("Website not found")
        return
