from models.core import Post
from tests.base import BaseTestCase


class PostTestCase(BaseTestCase):
    def test_create_post(self):
        ok, post = Post.create_or_update(
            author_id=2, title="帖子",
            content="好高兴呀")
        assert post.url() == '/post/1/'
        assert post.content == "好高兴呀"
