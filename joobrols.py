#! /usr/bin/env python3

import requests
import threading
from bs4 import BeautifulSoup
import argparse
from urllib.parse import urlparse


class Link:

    def __init__(self, path):
        self.path = path
        self.scraped = False
        self.broken = False
        self.sources = []

class Links:

    def __init__(self, base_url):
        self.base_url = base_url
        self.links = []
        self.lock = threading.Lock()

    def length(self):
        return len(self.links)

    def append(self, path):
        with self.lock:
            link = self.get(path)
            if not link:
                link = Link(path)
                self.links.append(link)
            return link

    def get(self, path):
        for l in self.links:
            if l.path == path:
                return l
        return None

all_links = None
max_links = 0
verbose = False
indent = 0

def scrape_page_thread(site, path):
    global indent
    global all_links

    link = all_links.append(path)
    if max_links != 0 and len(all_links.links) > max_links:
        if verbose:
            print("***", "  "*indent, "Ignored because of --max", path)
        return
    if link.scraped:
        if verbose:
            print("***", "  "*indent, "Already scraped", path)
        return
    else:
        link.scraped = True

    url = site+path
    if not verbose:
        #print('\r', len(all_links.links), "links", end="", flush=True)
        print('.', end="", flush=True)

    if not internal_link(path):
        if verbose:
            print("***", "  "*indent, "Reading external link", path)
        try:
            page = requests.get(path, timeout=10)
            if page.status_code != 200:
                # TODO handle redirects
                if verbose:
                    print("***", "  "*indent, "Broken, status_code = ", page.status_code)
                link.broken = True
        except:
            link.broken = True
        return
    else:
        if verbose:
            print("***", "  "*indent, "Reading internal link", path)
        try:
            page = requests.get(url, timeout=10)
            if not page:
                link.broken = True
                return
        except TimeoutError:
            link.broken = True
            return

    if verbose:
        print("***", "  "*indent, "Content-Type =", page.headers['content-type'])
    if not page.headers['content-type'].startswith('text/html;'):
        return

    soup = BeautifulSoup(page.content, 'html.parser')

    # Check for link to empty page in Joomla
    results = soup.find(id='content-area')
    if not results or len(results.contents) == 0 or (len(results.contents) == 1 and len(results.contents[0].strip()) == 0):
        link.broken = True
    
    if internal_link(link.path):
        discovered_links = soup.find_all('a')
        indent = indent + 1
        threads = []
        for l in discovered_links:
            discovered_url = l.get('href')
            if discovered_url and is_relevant_link(discovered_url):
                if verbose:
                    print("***", "  "*indent, "Discovered", discovered_url)
                threads.append(scrape_page(site, discovered_url))
                link = all_links.get(discovered_url)
                if link:
                    # Might be ignored because of --max
                    link.sources.append(path)
        indent = indent - 1
        for t in threads:
            t.join()

def is_relevant_link(discovered_url):
    return not discovered_url.startswith("#") \
        and not discovered_url.startswith("javascript") \
        and not discovered_url.endswith("print=1") \
        and not discovered_url.endswith("print=1&layout=default") \
        and not "component/mailto" in discovered_url

def internal_link(discovered_url):
    return not discovered_url.startswith("http")


def scrape_page(site, path):
    t = threading.Thread(target=scrape_page_thread, args=(site, path))
    t.start()
    return t

if (__name__ == "__main__"):

    argparser = argparse.ArgumentParser(
        description='Explore all links in a Joomla site and find which ones are broken or point to empty "pages"')
    argparser.add_argument(
        'url', help='URL to site')
    argparser.add_argument('--max', '-m', type=int, help='Maximum number of links to accumulate before analyzing')
    argparser.add_argument('--verbose', '-v', action='store_true')

    args = argparser.parse_args()

    if args.max:
        max_links = args.max
    
    if args.verbose:
        verbose = True

    parsed_url = urlparse(args.url)
    site = parsed_url.scheme+'://'+parsed_url.netloc
    print("Parsing pages from", site)
    all_links = Links(site)

    t = scrape_page(site, parsed_url.path)
    t.join()
    if not verbose:
        print("\nScraped", all_links.length(), "paths")
    else:
        print("scraped")

    broken_links = list(filter(lambda l: l.broken, all_links.links))
    print(len(broken_links), "broken paths found:")
    for link in broken_links:
        print("\t", link.path, "found in")
        for source in link.sources:
            print("\t\t", site+source)
    broken_links = list(filter(lambda l: l.broken, all_links.links))
    print(len(broken_links), "broken paths found")
