import establishConntection as connection
from bs4 import BeautifulSoup
import requests
import numpy as np



url = 'https://www.bbc.co.uk/news'
titleAndLink = []
imgurls = []
number_of_articles = 10

def bbcnewscontent():
    response = requests.get(url)
    if connection.status_code(response):
        content = response.content
        soup1 = BeautifulSoup(content, features="html.parser")
        coverpage_news = soup1.find_all(class_='gel-layout__item nw-c-top-stories__secondary-item gel-1/3@m gel-1/4@l nw-o-keyline nw-o-no-keyline@m')
        for n in np.arange(0, number_of_articles):
            link = coverpage_news[n].find('a', class_='nw-o-link-split__anchor')['href']
           
            title = coverpage_news[n].find('h3', class_='nw-o-link-split__text').get_text()
            #imgurl = coverpage_news[n].find(class_=".gs-o-responsive-image img")['src']
            if link[:4] != 'http':
                link = ''.join(("https://www.bbc.co.uk/", link))
            else:
               pass
            titleAndLink.append([title, link])
            #imgurls.append(imgurl)
            #table = {'IMG' : imgurls, 'TITLE' :titles, 'LINK' : links}
            #table = {'TITLE' :titles, 'LINK' : links}
        return titleAndLink
    elif response.status_code == 404:
        print("Website not found")
        return