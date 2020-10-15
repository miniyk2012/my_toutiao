from ext import db

from models.mixin import BaseMixin
from corelib.mc import cache, rdb

MC_KEY_COLLECT_N = 'collect_n:%s:%s'

class CollectItem(BaseMixin, db.Model):
    """收藏"""
    __tablename__ = 'collect_items'
    user_id = db.Column(db.Integer)
    target_id = db.Column(db.Integer)  # 收藏的目标id
    target_kind = db.Column(db.Integer)  # 收藏的种类, 比如post

    __table_args__ = (
        db.Index('idx_ti_tk_ui', target_id, target_kind, user_id),
    )

    @classmethod
    def __flush_event__(cls, target):
        """BaseModel里面配置了event, 会在增删改的时候把缓存清空"""
        rdb.delete(MC_KEY_COLLECT_N % (target.target_id, target.target_kind))

    # 读数据是用下缓存
    @classmethod
    @cache(MC_KEY_COLLECT_N % ('{target_id}', '{target_kind}'))
    def get_count_by_target(cls, target_id, target_kind):
        return cls.query.filter_by(target_id=target_id,
                                   target_kind=target_kind).count()

    @classmethod
    def get(cls, user_id, target_id, target_kind):
        return cls.query.filter_by(user_id=user_id, target_id=target_id,
                                   target_kind=target_kind).first()


class CollectMixin:
    def collect(self, user_id):
        """收藏功能, 如果self是post. 调用该函数, 就会建一条指向post的CollectItem"""
        item = CollectItem.get_by_target(user_id, self.id, self.kind)
        if item:
            return False
        ok, _ = CollectItem.create(user_id=user_id, target_id=self.id,
                                   target_kind=self.kind)
        return ok

    def uncollect(self, user_id):
        item = CollectItem.get_by_target(user_id, self.id, self.kind)
        if item:
            item.delete()
            return True
        return False

    @property
    def n_collects(self):
        return int(CollectItem.get_count_by_target(self.id, self.kind))

    def is_collected_by(self, user_id):
        return CollectItem.is_action_by(user_id, self.id, self.kind)



