import json
from abc import ABC, abstractmethod


class NewsTextRepository(ABC):
    
    @abstractmethod
    def persist(self, data):
        pass

class JsonFileRepository(NewsTextRepository):
    
    def __init__(self, path: str) -> None:
        self.path = path
    
    def persist(self, data):
        # abbreviate title, max 20 characters and file system friendly
        title = data['title'][:20].replace(' ', '_')
        date = data['date'].split(' ')[0]
        outfile = f"{data['symbol']}_{date}_{data['crawler']}_{title}.json"
        with open(outfile, 'w') as f:
            json.dump(data['text'], f, indent=4)
        print(f"Wrote file '{outfile}'")


class SqliteRepository(NewsTextRepository):
    
    def persist(self, data):        
        # insert data['text'] into News table using data['ticker] as FK from Tickers table
        ...
        
        
        
    

