from corelib.db import PropsItem
from corelib.mc import pcache, rdb, cache
from corelib.utils import cached_hybrid_property
from ext import db
from models.consts import K_COMMENT
from models.like import LikeMixin
from models.mixin import BaseMixin
from models.user import User

MC_KEY_COMMENT_LIST = 'comment_list:%s:%s'
MC_KEY_COMMENT_N = 'comment_list_n:%s:%s'


class Comment(BaseMixin, LikeMixin, db.Model):
    __tablename__ = 'comments'
    user_id = db.Column(db.Integer)
    target_id = db.Column(db.Integer)  # 评论的目标
    target_kind = db.Column(db.Integer)  # 评论目标的类型
    ref_id = db.Column(db.Integer, default=0)  # 引用其他人的评论, 可以不引用
    content = PropsItem('content', '')
    kind = K_COMMENT  # 自己是评论类型

    __table_args__ = (
        db.Index('idx_ti_tk_ui', target_id, target_kind, user_id),
    )

    @cached_hybrid_property
    def html_content(self):
        return self.content

    @cached_hybrid_property
    def user(self):
        return User.get(self.user_id)

    @classmethod
    def __flush_event__(cls, target):
        """BaseModel里面配置了event, 会在增删改的时候把缓存清空"""
        for key in (MC_KEY_COMMENT_LIST, MC_KEY_COMMENT_N):
            rdb.delete(key % (target.id, target.kind))


class CommentMixin(object):
    """收藏功能, 如果self是post. 调用该函数, 就会建一条指向post的Comment"""

    def add_comment(self, user_id, content, ref_id=None):
        _, obj = Comment.create(user_id=user_id, target_id=self.id,
                                target_kind=self.kind, ref_id=ref_id)
        obj.content = content
        return True

    def del_comment(self, user_id, comment_id):
        comment = Comment.get(comment_id)
        if comment and comment.user_id == user_id and \
                comment.target_id == self.id and comment.target_kind == self.kind:
            comment.delete()
            return True
        return False

    def get_comments(self, page, per_page):
        return self._get_comments(start=per_page * (page - 1), limit=per_page)

    @pcache(MC_KEY_COMMENT_LIST % ('{self.id}', '{self.kind}'))
    def _get_comments(self, start=0, limit=20):
        return Comment.query.filter_by(
            target_id=self.id, target_kind=self.kind).order_by(
            Comment.id.desc()).all()

    @property
    def n_comments(self):
        return self.get_n_comments()

    @cache(MC_KEY_COMMENT_N % ('{self.id}', '{self.kind}'))
    def get_n_comments(self):
        return Comment.get_count_by_target(self.id, self.kind)
