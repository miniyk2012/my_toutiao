import os
import unittest

os.environ["env"] = "test"

from app import app
from ext import db
from models.core import Post, PostTag, Tag
from models.collect import CollectItem
from models.comment import Comment
from models.contact import Contact, userFollowStats
from models.like import LikeItem
from models.user import User, Role


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.context = app.test_request_context()
        self.context.push()
        self.client = app.test_client()
        self.runner = app.test_cli_runner()
        db.drop_all()
        db.create_all()
        print('-' * 50)
        print('\n' * 5)

    def tearDown(self):
        print('\n' * 5)
        print('-' * 50)
        self.context.pop()
        with app.app_context():
            self.delete_all()
            db.drop_all()

    def delete_all(self):
        # delete的时候可以删除redis缓存
        for model in (Post, Tag, PostTag, CollectItem, Comment, Contact, userFollowStats, LikeItem, User, Role):
            for record in model.cache.filter():
                record.delete()
        # 数据库操作要通过SQLAlchemy，不要直接链接数据库操作
        db.session.commit()
