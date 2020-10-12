from sqlalchemy import text

from ext import db
from models.user import User
from tests.base import BaseTestCase


class MixinTestCase(BaseTestCase):
    def test_new_user(self):
        user = User()
        user.create_or_update(name='yangkai')
        result = db.session.execute(text('select * from users where name = :name'), {'name': 'yangkai'})
        print(result.fetchall())

        query_user = user.cache.filter(name='yangkai').first()
        assert query_user.name == 'yangkai'
        print(query_user.to_dict())

        query_user2 = user.cache.filter(name='yangkai').first()  # 第二次就能使用缓存了
        assert query_user2.name == 'yangkai'
