from tests.base import BaseTestCase

from sqlalchemy import text

from ext import db
from models.user import User


class MixinTestCase(BaseTestCase):
    def test_new_user(self):
        User.create_or_update(name='yangkaia')
        result = db.session.execute(text('select * from users where name = :name'), {'name': 'yangkai'})
        print(result.fetchall())

        query_user = User.cache.filter(name='yangkaia').first()

        assert query_user.name == 'yangkaia'
        print(query_user.to_dict())

        query_user2 = User.cache.filter(name='yangkaia').first()  # 第二次就能使用缓存了
        assert query_user2.name == 'yangkaia'

        # Todo: delete的时候可以删除redis缓存, 但不知为何query_user2.delete()会报错
        # query_user.delete()
        # print(1)
