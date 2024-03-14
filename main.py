


from crawlers.google_crawler import google_search
from crawlers.zack_crawler import ZackCrawler
from parsers import newspaper_parser
from utils.persistence import JsonFileRepository, SqliteRepository


if __name__ == "__main__":
    ticker = 'BAND'
    name = 'Bandwith Inc'
    date = '2022-11-02'
    #query = "Nutanix inc (NTNX) 2023-05-25"
    
    repo = JsonFileRepository('.')
    #repo = SqliteRepository()
    
    urls = google_search(f"{name} {ticker} {date}")
    newspaper_parser.parse(repo, 'google', ticker, urls, valid_date=date)
    
    # zc = ZackCrawler()     
    # urls = zc.earnings_extract(zc.earnings_crawler(ticker))
    # newspaper_parser.parse('zacks', ticker, urls)