import json
import time
from abc import ABC, abstractmethod


class PersistenceStrategy(ABC):
    
    @abstractmethod
    def persist(self, ticker, title, date, data):
        pass

class JsonPersistence(PersistenceStrategy):
    
    def persist(self, data):
        # abbreviate title, max 20 characters and file system friendly
        title = data['title'][:20].replace(' ', '_')
        date = data['date'].split(' ')[0]
        outfile = f"{data['ticker']}_{date}_json_{title}.json"
        with open(outfile, 'w') as f:
            json.dump(data['text'], f, indent=4)
        print(f"Wrote file '{outfile}'")


class SqlitePersistence(PersistenceStrategy):
    
    def persist(self, data):        
        # insert data['text'] into News table using data['ticker] as FK from Tickers table
        ...
        
        
        
    

