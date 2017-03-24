#!/usr/bin/env python
import requests
import hashlib
import random
from bs4 import BeautifulSoup
news_hashes = ["0"]

def get_yandex_news():
    url="https://news.yandex.ua/Kyiv/index.html?lang=ru"
    i = 0
    hexdigest = "0"
    while hexdigest in news_hashes and i < 10:
        i = i + 1
        request = requests.get(url)
        soup = BeautifulSoup(request.text,"lxml")
        titles = [h2.text for h2 in soup.findAll('div', attrs={'class': 'story__text'})]
        index = random.randrange(len(titles))
        news_string = titles[index]
        hash_object = hashlib.md5(news_string.encode('utf-8'))
        hexdigest = hash_object.hexdigest()

        if not hexdigest in news_hashes:
            news_hashes.append(hexdigest)
            return news_string

for i in range(10):
    print(i)
    print(get_yandex_news().encode('utf-8'))
#for t in titles:
#    print(t.encode('utf-8'))

#for div in soup.findAll('div',id='story__text'):
#    print "".join(div.findAll(text = True))
#list=soup.find("div", {"id": "story__text"})
#if list:
#    print(list)


