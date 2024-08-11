
from datetime import datetime, timedelta

from analysts.prompt import OPEN_AI_PROMPT_ONE
from crawlers.google_crawler import google_search
from crawlers.zack_crawler import ZackCrawler
from parsers import newspaper_parser
from utils.persistence import JsonFileRepository, SqliteRepository
import asyncio

search_semaphore = asyncio.Semaphore(1)
main_semaphore = asyncio.Semaphore(2)

async def aget_descriptions(db: SqliteRepository):
    return await db.get_company_desc_all()

def get_descriptions(db: SqliteRepository):
    return db.get_company_desc_all()

async def limited_sip_search(sym, company_name, date):
    async with main_semaphore:
        return await sip_search(sym, company_name, date)

async def sip_search(ticker: str, name: str, date: str, search='google'):
    d1 = date
    d0 = f"{datetime.strptime(d1, '%Y-%m-%d') - timedelta(days=1)}"[:10]
    d2 = f"{datetime.strptime(d1, '%Y-%m-%d') + timedelta(days=1)}"[:10]
    
    print(f"{ticker}: google search ({name}) on {d1}")
    q = f"{name} ({ticker}) {d1}"
    if search == 'google':
        async with search_semaphore:
            urls = await google_search(q, ticker)
    else:
        raise ValueError(f"Unknown search engine: {search}")
    
    print(f"{ticker}: Parsing {len(urls)} urls for ({name}) on {d1}")
    tasks = [newspaper_parser.a_parse('google', ticker, url, valid_dates=[d0, d1, d2]) for url in urls]
    results = await asyncio.gather(*tasks)
    
    # JSON
    print(f"{ticker}: Persisting (JSON) {len(results)} parsed results for {ticker} ({name}) on {d1}")            
    tasks = [json_repo.a_persist(r) for r in results if r]    
    results = await asyncio.gather(*tasks) 
    
    #SQLite
    print(f"{ticker}: Persisting (SQLite) {len(results)} parsed results for {ticker} ({name}) on {d1}")            
    tasks = [db_repo.a_persist(r) for r in results if r]    
    results = await asyncio.gather(*tasks)
    
    print(f"{ticker}: Persisted {len(results)} parsed results for {ticker} ({name}) on {d1}")   
    

    
if __name__ == "__main__":
    db_repo = SqliteRepository('/Users/fbjarkes/git/tickers-db/db/sqlite/tickers.sqlite')
    json_repo = JsonFileRepository('.')
    company_names = db_repo.get_company_desc_all()
    
    # loop = asyncio.get_event_loop()
    # eps = ['PHUN: 2021-10-22', 'NTNX: 2023-05-25', 'AKBA: 2017-04-25']
    # tasks = []
    
    # for ep in eps:
    #     sym, date = ep.split(':')
    #     tasks.append(limited_sip_search(sym, company_names[sym], date)) 
    # loop.run_until_complete(asyncio.gather(*tasks))  

    
    # loop = asyncio.get_event_loop()
    # #ticker = 'PHUN'
    # #name = 'Phunware Inc'
    # #date = '2021-10-22'
    # #query = "Nutanix inc (NTNX) 2023-05-25"
    # symbol_desc = loop.run_until_complete(get_descriptions(db_repo))    
        
    # ticker = 'AKBA'
    # name = 'Akebia Therapeutics Inc'
    # d1 = '2017-04-25'
    
    # d0 = f"{datetime.strptime(d1, '%Y-%m-%d') - timedelta(days=1)}"[:10]
    # d2 = f"{datetime.strptime(d1, '%Y-%m-%d') + timedelta(days=1)}"[:10]

    # # TODO finviz screener för lite manuell checking av moves
    
    
    # #db_repo = SqliteRepository('/Users/fbjarkes/git/tickers-db/db/sqlite/tickers.sqlite')
    # #name = db_repo.get(ticker)
    
    # # Yahoo Finance
    # #urls = yfinance_search(ticker) 
    # #newspaper_parser.parse(repo, 'yahoo', ticker, urls)
    
    # # Crawling based on news and date
    # # TODO: async for each ticker from file list:
    # #urls = google_search(f"{name} ({ticker}) {d0} {d1} {d2}")
    # print(80*'=')
    # print(f"{ticker}: google search ({name}) on {d1}")
    # q = f"{name} ({ticker}) {d1}"
    # urls = google_search(q, ticker)
    
    # print(f"{ticker}: Parsing {len(urls)} urls for ({name}) on {d1}")
    # tasks = [newspaper_parser.a_parse('google', ticker, url, valid_dates=[d0, d1, d2]) for url in urls]
    # #results = await asyncio.gather(*tasks)
    # results =loop.run_until_complete(asyncio.gather(*tasks))
    
    # # JSON
    # print(f"{ticker}: Persisting (JSON) {len(results)} parsed results for {ticker} ({name}) on {d1}")            
    # tasks = [json_repo.a_persist(r) for r in results if r]    
    # results =loop.run_until_complete(asyncio.gather(*tasks))  
    
    # #SQLite
    # print(f"{ticker}: Persisting (SQLite) {len(results)} parsed results for {ticker} ({name}) on {d1}")            
    # tasks = [db_repo.a_persist(r) for r in results if r]    
    # results =loop.run_until_complete(asyncio.gather(*tasks))  
    
    # loop.close()     
    
    # # # Crawling based on ERs
    # # #zc = ZackCrawler()     
    # # #urls = zc.earnings_extract(zc.earnings_crawler(ticker))
    # # #newspaper_parser.parse(repo, 'zacks', ticker, urls, max_urls=20)
    
    # # articles = repo.get(ticker, date=d1)    
    # # for a in articles:
    # #     summary = OpenAISummarizer('...', prompt=OPEN_AI_PROMPT_ONE).summarize(a.text)
    # #     a['summary'] = summary
    # #     repo.persist(a)

        
        