import json
import os
import requests
import time
from datetime import datetime
from src.crawler import UtkCrawler
from src.models import Article, History
from settings import DISCORD_WEBHOOK_URL, HISTORY_JSON_PATH, WATCH_INTERVAL_MINUTES


def save_history(latest_articles: list[Article]):
    history = History(
        latest_articles=latest_articles,
        updated_at=datetime.now()
    )
    with open(HISTORY_JSON_PATH, 'w') as f:
        f.write(history.json(ensure_ascii=False, indent=2))


def load_history() -> History:
    if not os.path.exists(HISTORY_JSON_PATH):
        save_history([])
    with open(HISTORY_JSON_PATH, 'r') as f:
        return History(**json.load(f))


def send_message_to_discord(new_article: Article):
    payload = {
        'content': '新しいお知らせがあります。',
        'embeds': [
            {
                'title': new_article.title,
                'url': new_article.url,
                'description': new_article.content,
                'timestamp': new_article.published_at.isoformat()
            }
        ]
    }
    res = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    res.raise_for_status()


def main():
    history = load_history()
    old_articles = history.latest_articles

    crawler = UtkCrawler()
    fetched_articles = crawler.fetch_articles()

    new_articles = set(fetched_articles) - set(old_articles)
    new_articles = sorted(
        list(new_articles),
        key=lambda x: x.published_at, reverse=True
    )

    if new_articles:
        save_history(fetched_articles)

    for article in new_articles:
        send_message_to_discord(article)


if __name__ == '__main__':
    while True:
        main()
        time.sleep(WATCH_INTERVAL_MINUTES * 60)
