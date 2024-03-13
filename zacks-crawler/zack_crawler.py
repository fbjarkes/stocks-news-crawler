from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
    

class ZackCrawler:
    
    def __init__(self) -> None:
        self.base_url_earnings = """https://www.zacks.com/stock/research/{}/earnings-headlines?icid=quote-stock_overview-quote_nav_tracking-zcom-left_subnav_quote_navbar-earning_news"""
        self.base_url = "https://www.zacks.com"

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107 Safari/537.36'
        }
    def earnings_crawler(self, ticker: str):
        url = self.base_url_earnings.format(ticker)        
        print(f"Fetching URL: '{url}'")
        
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.text
        else:
            print("Failed to fetch HTML data:", response.status_code)
            return None

    def earnings_extract(self, html_data: str):
        if html_data is None:
            return []
        print(f"Parsing for {len(html_data)} chars")
        urls = []
        soup = BeautifulSoup(html_data, 'html.parser')
        comp_news_section = soup.find('section', id='comp_news')
        if comp_news_section:
            ul_elements = comp_news_section.find_all('ul')
            for ul in ul_elements:
                li_elements = ul.find_all('li')
                for li in li_elements:
                    a_tag = li.find('a')
                    if a_tag:                                                
                        url = a_tag.get('href')    
                        if url.startswith('/research/get_news.php'):
                            full_url = urljoin(self.base_url, f"{url}&art_rec=quote-quote-earnings_news-ID02-txt")
                        else:
                            full_url = urljoin(self.base_url, url)                        
                        
                        print(f"Found URL: {full_url}")
                        urls.append(full_url)

        return urls
        


if __name__ == "__main__":
    zc = ZackCrawler()
    
    
    urls = zc.earnings_extract(zc.earnings_crawler('JOBY'))
    print(urls)
    print("Done")