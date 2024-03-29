


import datetime
import time
from typing import List

import newspaper

from utils.persistence import NewsTextRepository


def validate_article_date(art: newspaper.Article, valid_date: str):
    if not valid_date:
        return True
    if art.publish_date is None:
        raise ValueError("Article publish_date is None")
    #date = f"{art.publish_date}"

    publish_date = art.publish_date.date()
    valid_date = datetime.strptime(valid_date, "%Y-%m-%d").date()

    start_date = valid_date - datetime.timedelta(days=1)
    end_date = valid_date + datetime.timedelta(days=1)
    if not start_date <= publish_date <= end_date:
        raise ValueError(f"Article publish_date {art.publish_date} does not match valid_date {valid_date}")
    

def validate_article_text(art: newspaper.Article):
    if art.text is None or len(art.text) < 100:
        raise ValueError("Article text is None")


def parse(repository: NewsTextRepository, crawler: str, ticker: str, urls: List[str], valid_date=''):
    for url in urls:
        print('='*80)
        print(f"Processing URL: {url}")
        
        try: 
            article = newspaper.article(url)
            validate_article_date(article, valid_date)    
            validate_article_text(article)
        except ValueError as e:
            print(f"Invalid article: {e} ({url})")
            continue
        except Exception as e:
            print(f"Failed to parse URL: {e} ({url})")
            continue
        
        date = f"{article.publish_date}"        
        data = {'symbol': ticker, 'text': article.text, 'date': f"{date}", 'url': url, 'title': article.title, 'crawler': crawler}        
        
        repository.persist(data)
        
        time.sleep(3)
        