


from datetime import datetime, timedelta
import time
from typing import List

import newspaper

from model import ArticleData
from utils.persistence import NewsTextRepository

def get_random_headers():
    ...#TODO: return randomize non scraping looking headers

def validate_article_date(art: newspaper.Article, valid_date: str):
    if not valid_date:
        return True
    if art.publish_date is None:
        raise ValueError("Article publish_date is None")
    #date = f"{art.publish_date}"

    publish_date = art.publish_date.date()
    valid_date = datetime.strptime(valid_date, "%Y-%m-%d").date()

    start_date = valid_date - timedelta(days=1)
    end_date = valid_date + timedelta(days=1)
    if not start_date <= publish_date <= end_date:
        raise ValueError(f"Article publish_date {art.publish_date} does not match valid_date {valid_date}")
    
def validate_article_dates(art: newspaper.Article, valid_dates: List[str]):    
    if art.publish_date is None:
        raise ValueError("Article publish_date is None")
    
    d = f"{art.publish_date.date()}"[:10]    
    if d not in valid_dates:
        raise ValueError(f"Article publish_date {art.publish_date} does not match valid_dates {valid_dates}")
    

def validate_article_text(art: newspaper.Article):
    if art.text is None or len(art.text) < 100:
        raise ValueError("Article text is None")


def parse(repository: NewsTextRepository, crawler: str, ticker: str, urls: List[str], valid_date=''):
    i = 0
    for url in urls:
        i += 1
        print('='*80)
        print(f"Processing URL ({i}): {url}")
        
        try: 
            article = newspaper.article(url)
            validate_article_date(article, valid_date)    
            validate_article_text(article)
        except ValueError as e:
            print(f"Invalid article: {e} ({url})")
            continue
        except Exception as e:
            #TODO: if 403 then retry with other headers? (https://www.biopharmcatalyst.com/company/AKBA)
            print(f"Failed to parse URL: {e} ({url})")
            continue
        
        date = f"{article.publish_date}"        
        #data = {'symbol': ticker, 'text': article.text, 'date': f"{date}", 'url': url, 'title': article.title, 'crawler': crawler} #TODO: model       
        data = ArticleData(symbol=ticker, text=article.text, date=f"{date}", url=url, title=article.title, crawler=crawler)
        
        repository.persist(data)
        
        time.sleep(3)
        
async def a_parse(crawler: str, ticker: str, url: str, valid_dates: List[str]) -> ArticleData:
    print(f"{ticker}: Processing URL: '{url}'")
    
    try: 
        article = newspaper.article(url)
        validate_article_dates(article, valid_dates)    
        validate_article_text(article)
    except ValueError as e:        
        print(f"{ticker}: Invalid article: {e} ({url})")
        return None
    except Exception as e:
        #TODO: if 403 then retry with other headers? (https://www.biopharmcatalyst.com/company/AKBA)
        print(f"{ticker}: Failed to parse URL: {e} ({url})")
        return None
    
    date = f"{article.publish_date}"        
    data = ArticleData(symbol=ticker, text=article.text, date=f"{date}", url=url, title=article.title, crawler=crawler)
    print(f"{ticker}: Successful ArticleData '{data.title}' ({len(data.text)} chars) ({data.date})")
    return data
