import requests
from datetime import datetime
from bs4 import BeautifulSoup
from bs4.element import ResultSet as BS4ResultSet

from .models import Article


class UtkCrawler:
    def __init__(self) -> None:
        self.session = requests.Session()
        articles_url = 'http://www.tochigi-edu.ed.jp/utsunomiya/nc2/?page_id=34'
        self.articles_page = self.session.get(articles_url)
        self.articles_page.raise_for_status()

        self.soup = BeautifulSoup(self.articles_page.text, 'html.parser')

    def __extract_article_elements(self) -> BS4ResultSet:
        articles = self.soup.select('div[id^=journal_detail]')
        return articles

    def fetch_articles(self) -> list[Article]:
        article_els = self.__extract_article_elements()

        articles: list[Article] = []
        for article_el in article_els:
            title = article_el.select_one('a').text
            content = article_el.select_one(
                'div[class="journal_content"]').text
            url = article_el.select_one('a')['href']
            date_raw = article_el.select_one(
                'th[class="journal_list_date"]').text
            published_at = datetime.strptime(date_raw, '%Y/%m/%d').date()

            articles.append(Article(
                title=title,
                content=content,
                url=url,
                published_at=published_at
            ))

        return articles
