#! /bin/env python3

import requests
from bs4 import BeautifulSoup
import argparse
from urllib.parse import urlparse

all_internal_links = []

def scrape_page(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='content-area')
    if len(results.contents) == 0:
        print("Main page is empty")
    else:
        links = soup.find_all('a')
        for l in links:
            link = l.get('href')
            if link != "/"  and not link.startswith("http") and not link.startswith("#") and not link.startswith("javascript"):
                print(link)

if (__name__ == "__main__"):

    argparser = argparse.ArgumentParser(
        description='Explore all internal links in a Joomla site and find which ones point to empty "pages"')
    argparser.add_argument(
        'url', help='URL to site')

    args = argparser.parse_args()

    parsed_url = urlparse(args.url)
    site = parsed_url.scheme+'://'+parsed_url.netloc
    print("Parsing pages from", site)

    scrape_page(args.url)
