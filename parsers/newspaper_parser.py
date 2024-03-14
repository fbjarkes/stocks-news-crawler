


import time
from typing import List

import newspaper

from utils.persistence import PersistenceStrategy


def validate_article_date(art: newspaper.Article, valid_date: str):
    if not valid_date:
        return True
    if art.publish_date is None:
        raise ValueError("Article publish_date is None")
    date = f"{art.publish_date}"
    date = date.split(' ')[0]
    if date != valid_date:
        raise ValueError(f"Article publish_date {art.publish_date} does not match valid_date {valid_date}")
    

def validate_article_text(art: newspaper.Article):
    if art.text is None or len(art.text) < 100:
        raise ValueError("Article text is None")


def parse(repository: PersistenceStrategy, parser: str, ticker: str, urls: List[str], valid_date=''):
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
        
  
        # format date like '2023-02-22'
        date = f"{article.publish_date}"        
        data = {'symbol': ticker, 'text': article.text, 'date': f"{date}", 'url': url, 'title': article.title}
        
        repository.persist(data)
        
        time.sleep(3)
        