from dataclasses import dataclass
from datetime import datetime
from html.parser import HTMLParser
import random
import feedparser

from app import app
from models.core import Post, PostTag, Tag, db
from models.search import Item


class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def fetch(url):
    d = feedparser.parse(url)
    entries = d.entries

    for entry in entries:
        try:
            content = entry.content and entry.content[0].value
        except AttributeError:
            content = entry.summary or entry.title
        try:
            created_at = datetime.strptime(entry.published, '%Y-%m-%dT%H:%M:%S.%fZ')
        except ValueError:
            created_at = datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %z')
        try:
            tags = entry.tags
        except AttributeError:
            @dataclass
            class Tag:
                term: str

            tags = random.sample([Tag('python'), Tag('amazon'), Tag('golang'), Tag('php'), Tag('docker'), Tag('wechat'),
                                  Tag('android'), Tag('wiki'), Tag('c++'), Tag('k8s'), Tag('mac'), Tag('linux'),
                                  Tag('HDFS')],
                                 k=random.randint(0, 5))

        ok, _ = Post.create_or_update(
            author_id=6, title=entry.title, orig_url=entry.link,
            content=strip_tags(content), created_at=created_at,
            tags=[tag.term for tag in tags])


def main():
    with app.test_request_context():
        Item._index.delete(ignore=404)  # 删除Elasticsearch索引，销毁全部数据
        Item.init()
        for model in (Post, Tag, PostTag):
            model.query.delete()  # 数据库操作要通过SQLAlchemy，不要直接链接数据库操作, 这样才能正确的触发事件(如清3缓存, 清es索引)
        db.session.commit()

        for site in (
                'http://www.dongwm.com/atom.xml',):
            fetch(site)


if __name__ == '__main__':
    main()
    with app.test_request_context():
        post = Post.query.first()
        print(post.content)
        print(post.title)
