from dataclasses import dataclass

@dataclass
class ArticleData:
    symbol: str
    text: str
    date: str
    url: str
    title: str
    crawler: str