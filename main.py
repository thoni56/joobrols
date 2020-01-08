#! /bin/env python3

import requests
from bs4 import BeautifulSoup

URL = 'https://events.responsive.se/'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
results = soup.find(id='content-area')
if len(results.contents) == 0:
    print("Main page is empty")
else:
    links = soup.find_all('a')
    for l in links:
        print(l.get('href'))
    