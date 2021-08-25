from pydantic import BaseModel
from datetime import datetime, date

__all__ = ['Article', 'History']


class HashableBaseModel(BaseModel):
    def __hash__(self) -> int:
        return hash((type(self),) + tuple(self.__dict__.values()))


class Article(HashableBaseModel):
    title: str
    content: str
    url: str
    published_at: date


class History(BaseModel):
    latest_articles: list[Article]
    updated_at: datetime
