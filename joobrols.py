#! /bin/env python3

import requests
from bs4 import BeautifulSoup
import argparse
from urllib.parse import urlparse


class Link:

    def __init__(self, path):
        self.path = path
        self.scraped = False

class Links:

    def __init__(self, base_url):
        self.base_url = base_url
        self.links = []

    def length(self):
        return len(self.links)

    def append(self, path):
        if not self.get(path):
            self.links.append(Link(path))

    def get(self, path):
        for l in self.links:
            if l.path == path:
                return l
        return None


all_links = None

def scrape_page(site, path):
    all_links.append(path)
    if all_links.get(path).scraped:
        return
    else:
        all_links.get(path).scraped = True
    print("Scraping", path)
    url = site+path
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Check for broken link
    results = soup.find(id='content-area')
    if not results or len(results.contents) == 0:
        # TODO: mark path as broken
        print(path, " is empty")
    
    discovered_links = soup.find_all('a')
    for l in discovered_links:
        discovered_url = l.get('href')
        if discovered_url and is_relevant_link(discovered_url):
            scrape_page(site, discovered_url)

def is_relevant_link(discovered_url):
    return not discovered_url.startswith("http") \
        and not discovered_url.startswith("#") \
        and not discovered_url.startswith("javascript") \
        and not discovered_url.endswith(".pdf") \
        and not discovered_url.endswith(".jpg") \
        and not discovered_url.endswith("print=1") \
        and not "component/mailto" in discovered_url
        
if (__name__ == "__main__"):

    argparser = argparse.ArgumentParser(
        description='Explore all internal links in a Joomla site and find which ones point to empty "pages"')
    argparser.add_argument(
        'url', help='URL to site')

    args = argparser.parse_args()

    parsed_url = urlparse(args.url)
    site = parsed_url.scheme+'://'+parsed_url.netloc
    print("Parsing pages from", site)
    all_links = Links(site)

    scrape_page(site, parsed_url.path)
    print("Scraped", all_links.length(), "paths")