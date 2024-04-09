import asyncio
import sys
sys.path.insert(0, '/Users/fbjarkes/git/python/stock-catalyst-news-crawler') # so we can run this file

import json
from bs4 import BeautifulSoup
import requests
import re
import mechanicalsoup

from parsers import newspaper_parser

async def agoogle_search(query):
    browser = mechanicalsoup.StatefulBrowser()
    urls = []
    
    browser.session.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }
    
    browser.open("https://www.google.com/")
    browser.select_form('form[action="/search"]')
    browser["q"] = query
    browser.submit_selected()

    search_results = browser.get_current_page().select('.tF2Cxc')
    print(f"Found {len(search_results)} results for '{query}'")
    for idx, result in enumerate(search_results, start=1):
        title = result.select_one('.DKV0Md').text
        #TODO: can get summary and date already here? or do fast AI filter on relevance?
        url = result.select_one('a')['href']
        print(f"Result {idx}: {title} - {url}")
        urls.append(url)
    
    return urls

def google_search(query):
    browser = mechanicalsoup.StatefulBrowser()
    urls = []
    
    browser.session.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }
    
    browser.open("https://www.google.com/")
    browser.select_form('form[action="/search"]')
    browser["q"] = query
    browser.submit_selected()

    search_results = browser.get_current_page().select('.tF2Cxc')
    print(f"Found {len(search_results)} results for '{query}'")
    for idx, result in enumerate(search_results, start=1):
        title = result.select_one('.DKV0Md').text
        #TODO: can get summary and date already here? or do fast AI filter on relevance?
        url = result.select_one('a')['href']
        print(f"Result {idx}: {title} - {url}")
        urls.append(url)
    
    return urls

if __name__ == "__main__":
    query = "BAND Bandwidth Inc 2022-11-02"
    #query = "Nutanix inc (NTNX) 2023-05-25"
    #urls = google_search(query)
    #newspaper_parser.parse('google', 'NTNX', urls, valid_date='2023-05-25')

    urls = asyncio.run(agoogle_search(query))
    for url in urls:
        print(url)
    
