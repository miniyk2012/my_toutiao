import os

from corelib.db import PropsItem
from corelib.mc import rdb
from corelib.utils import is_numeric
from ext import db
from models.comment import CommentMixin
from models.consts import K_POST
from models.mixin import BaseMixin

MC_KEY_ALL_TAGS = 'core:all_tags'
MC_KEY_POSTS_BY_TAG = 'core:posts_by_tags:%s:%s'
MC_KEY_POST_STATS_BY_TAG = 'core:count_by_tags:%s'

PER_PAGE = 2
HERE = os.path.abspath(os.path.dirname(__file__))


class Post(BaseMixin, CommentMixin, db.Model):
    __tablename__ = 'posts'
    author_id = db.Column(db.Integer)
    title = db.Column(db.String(128), default='')
    orig_url = db.Column(db.String(255), default='')
    can_comment = db.Column(db.Boolean, default=True)
    content = PropsItem('content', '')
    kind = K_POST

    __table_args__ = (
        db.Index('idx_title', title),
    )

    def url(self):
        return '/{}/{}/'.format(self.__class__.__name__.lower(), self.id)

    @classmethod
    def __flush_event__(cls, target):
        rdb.delete(MC_KEY_ALL_TAGS)

    @classmethod
    def get(cls, identifier):
        if is_numeric(identifier):
            return cls.cache.get(identifier)
        return cls.cache.filter(title=identifier).first()

    @property
    # TODO cache
    def tags(self):
        at_ids = PostTag.query.with_entities(
            PostTag.tag_id).filter(
            PostTag.post_id == self.id
        ).all()

        tags = Tag.query.filter(Tag.id.in_((id for id, in at_ids))).all()
        return tags


class Tag(BaseMixin, db.Model):
    __tablename__ = 'tags'
    name = db.Column(db.String(128), default='', unique=True)

    __table_args__ = (
        db.Index('idx_name', name),
    )


class PostTag(BaseMixin, db.Model):
    __tablename__ = 'post_tags'
    post_id = db.Column(db.Integer)
    tag_id = db.Column(db.Integer)

    __table_args__ = (
        db.Index('idx_post_id', post_id, 'updated_at'),
        db.Index('idx_tag_id', tag_id, 'updated_at'),
    )
