#! /bin/env python3

import requests
from bs4 import BeautifulSoup
import argparse
from urllib.parse import urlparse


class Link:

    def __init__(self, url):
        self.url = url
        self.scraped = False

class Links:

    def __init__(self, base_url):
        self.base_url = base_url
        self.links = []

    def length(self):
        return len(self.links)

    def append(self, url):
        self.links.append(Link(url))


all_internal_links = None

def scrape_page(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='content-area')
    if len(results.contents) == 0:
        print("Main page is empty")
    else:
        discovered_links = soup.find_all('a')
        for l in discovered_links:
            discovered_url = l.get('href')
            if discovered_url != "/"  and not discovered_url.startswith("http") and not discovered_url.startswith("#") and not discovered_url.startswith("javascript"):
                all_internal_links.append(discovered_url)
        # TODO: mark this url as scraped
        
if (__name__ == "__main__"):

    argparser = argparse.ArgumentParser(
        description='Explore all internal links in a Joomla site and find which ones point to empty "pages"')
    argparser.add_argument(
        'url', help='URL to site')

    args = argparser.parse_args()

    parsed_url = urlparse(args.url)
    site = parsed_url.scheme+'://'+parsed_url.netloc
    print("Parsing pages from", site)
    all_internal_links = Links(site)

    scrape_page(args.url)
