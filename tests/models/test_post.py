from tests.base import BaseTestCase
from models.core import Post


class PostTestCase(BaseTestCase):
    def test_create_post(self):
        ok, post = Post.create_or_update(
            author_id=2, title="帖子",
            content="好高兴呀")
        assert post.url() == '/post/1/'
        assert post.content == "好高兴呀"
        # query_post = Post.query.filter_by(id=post.id).first()
        query_post = Post.query.filter(Post.id == post.id).first()
        assert query_post.url() == '/post/1/'
        # Post继承了db.Model, 而db.Model在ext.py里被设置成BaseModel, BaseModel能正常处理保存在redis中的字段
        assert query_post.content == "好高兴呀"
