import json
from abc import ABC, abstractmethod
from typing import Dict

import aiofiles
import aiosqlite

from model import ArticleData


class NewsTextRepository(ABC):
    
    @abstractmethod
    def persist(self, data: ArticleData):
        pass
    
    @abstractmethod
    async def a_persist(self, data: ArticleData):
        pass

class JsonFileRepository(NewsTextRepository):
    
    def __init__(self, path: str) -> None:
        self.path = path
    
    def persist(self, data: ArticleData):
        # abbreviate title, max 20 characters and file system friendly
        title = data.title[:20].replace(' ', '_')
        date = data.date.split(' ')[0]
        outfile = f"{data.symbol}_{date}_{data.crawler}_{title}.json"
        with open(outfile, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Wrote file '{outfile}'")
    
        
    async def a_persist(self, data: ArticleData):
        # abbreviate title, max 20 characters and file system friendly
        title = data.title[:20].replace(' ', '_')
        date = data.date.split(' ')[0]
        outfile = f"{data.symbol}_{date}_{data.crawler}_{title}.json"
        async with aiofiles.open(outfile, 'w') as f:
            await f.write(json.dumps(data, indent=4))
        print(f"Wrote file '{outfile}'")


class SqliteRepository(NewsTextRepository):
 
    
    def __init__(self, db_path, table='tickers'):
        self.db_path = db_path
        self._conn = None
        self.table = table
        
    async def connect(self):    
        self._conn = await aiosqlite.connect(self.db_path)


    async def __aenter__(self):        
        await self.connect()
        return self


    async def __aexit__(self, exc_type, exc_val, exc_tb):            
        await self._conn.close()


    def persist(self, data):        
        # insert data['text'] into News table using data['ticker] as FK from Tickers table
        ...
    
    
    async def a_persist(self, data: ArticleData):
        pass    
    
    
    async def get_company_desc(self, symbol):    
        async with self:
            cursor = await self._conn.cursor()
            await cursor.execute(f"SELECT company_desc FROM {self.table} WHERE {symbol} = ?", (symbol))
            row = await cursor.fetchone()
            return row[0] if row else ''
        
    async def get_company_desc_all(self) -> Dict[str, str]:
        async with self:
            cursor = await self._conn.cursor()
            await cursor.execute(f"SELECT * FROM {self.table}")
            rows = await cursor.fetchall()        
            return {row[0]: row[1] for row in rows}

        
        
        
    

