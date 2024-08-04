import json
from abc import ABC, abstractmethod
import sqlite3
from typing import Dict, List

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
            json.dump(data.__dict__, f, indent=4)  # Convert data to a dictionary
        print(f"Wrote file '{outfile}'")
    
        
    async def a_persist(self, data: ArticleData):
        # abbreviate title, max 20 characters and file system friendly
        title = data.title[:20].replace(' ', '_')
        date = data.date.split(' ')[0]
        outfile = f"{data.symbol}_{date}_{data.crawler}_{title}.json"
        async with aiofiles.open(outfile, 'w') as f:
            await f.write(json.dumps(data.__dict__, indent=4))
        print(f"Wrote file '{outfile}'")


# class SqliteRepository(NewsTextRepository):
 
#     def __init__(self, db_path, table='tickers'):
#         self.db_path = db_path
#         self._conn = None
#         self.table = table
        
#     async def connect(self):    
#         self._conn = await aiosqlite.connect(self.db_path)

#     def connect(self):    
#         self._conn = aiosqlite.connect(self.db_path)

#     async def __aenter__(self):        
#         await self.connect()
#         return self


#     async def __aexit__(self, exc_type, exc_val, exc_tb):            
#         await self._conn.close()


#     def persist(self, data):        
#         # insert data['text'] into News table using data['ticker] as FK from Tickers table
#         with self._conn:
#             cursor = self._conn.cursor()
#             cursor.execute(f"INSERT INTO {self.table} (symbol, company_desc) VALUES (?, ?)", (data['symbol'], data['text']))


#     async def apersist(self, data: ArticleData):
#         async with self:
#             cursor = await self._conn.cursor()
#             await cursor.execute(f"INSERT INTO {self.table} (symbol, company_desc) VALUES (?, ?)", (data.symbol, data.text))


#     async def get_company_desc(self, symbol):    
#         async with self:
#             cursor = await self._conn.cursor()
#             await cursor.execute(f"SELECT company_desc FROM {self.table} WHERE {symbol} = ?", (symbol))
#             row = await cursor.fetchone()
#             return row[0] if row else ''
    
#     def get_company_desc(self, symbol):
#         with self._conn:
#             cursor = self._conn.cursor()
#             cursor.execute(f"SELECT company_desc FROM {self.table} WHERE {symbol} = ?", (symbol))
#             row = cursor.fetchone()
#             return row[0] if row else ''
        
    
#     async def aget_company_desc_all(self) -> Dict[str, str]:
#         async with self:
#             cursor = await self._conn.cursor()
#             await cursor.execute(f"SELECT * FROM {self.table}")
#             rows = await cursor.fetchall()        
#             return {row[0]: row[1] for row in rows}
    
    
#     def get_company_desc_all(self) -> Dict[str, str]:
#         with self._conn:
#             cursor = self._conn.cursor()
#             cursor.execute(f"SELECT * FROM {self.table}")
#             rows = cursor.fetchall()        
#             return {row[0]: row[1] for row in rows}



class SqliteRepository(NewsTextRepository):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_path)

    def close(self):
        if self.connection:
            self.connection.close()

    def persist(self, data: ArticleData):
        if not self.connection:
            raise RuntimeError("Database connection is not established.")
        
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO articles (title, content) VALUES (?, ?)", (data.title, data.content))

    async def a_persist(self, data: ArticleData):
        if not self.connection:
            raise RuntimeError("Database connection is not established.")
        
        async with self.connection:
            cursor = self.connection.cursor()
            await cursor.execute("INSERT INTO articles (title, content) VALUES (?, ?)", (data.title, data.content))

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    #====== 
    def get_company_names(self) -> List[str]:
        if not self.connection:
            raise RuntimeError("Database connection is not established.")
        
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute("SELECT company_name FROM tickers")
            result = cursor.fetchall()
            return [row[0] for row in result]
    
    

