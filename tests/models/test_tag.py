from models.core import Tag
from tests.base import BaseTestCase


class TagTestCase(BaseTestCase):
    def test_create_tag(self):
        ok, tag = Tag.create(name='yangkai')
        assert ok is True
        ok2, tag2 = Tag.create(name='yangkai')
        assert ok2 is False
        assert tag is tag2
