from collections import defaultdict

from elasticsearch_dsl import Document, Integer, Text, Boolean, Q, Keyword, SF, Date
from elasticsearch_dsl.connections import connections
from elasticsearch.helpers import parallel_bulk
from elasticsearch.exceptions import ConflictError
from flask_sqlalchemy import Pagination

from corelib.mc import rdb, cache

from config import ES_HOSTS, PER_PAGE
from models.consts import K_POST, ONE_HOUR
from models.core import Post

connections.create_connection(hosts=ES_HOSTS)

ITEM_MC_KEY = 'core:search:{}:{}'
POST_IDS_BY_TAG_MC_KEY = 'core:search:post_ids_by_tag:%s:%s:%s:%s'
SEARCH_FIELDS = ['title^10', 'tags^5', 'content^2']
gauss_sf = SF('gauss', created_at={
    'origin': 'now', 'offset': '7d', 'scale': '10d'
})

score_sf = SF('script_score', script={
    'lang': 'painless',
    'inline': ("doc['n_likes'].value * 2 + doc['n_collects'].value")
})

TARGET_MAPPER = {
    K_POST: Post
}


def get_item_data(item):
    """item是Post model的对象"""
    try:
        content = item.content
    except AttributeError:
        content = ''

    try:
        tags = [tag.name for tag in item.tags]
    except AttributeError:
        tags = []

    return {
        'id': item.id,
        'tags': tags,
        'content': content,
        'title': item.title,
        'kind': item.kind,
        'n_likes': item.n_likes,
        'n_comments': item.n_comments,
        'n_collects': item.n_collects,
    }


class Item(Document):
    title = Text()
    kind = Integer()
    content = Text()
    n_likes = Integer()
    n_collects = Integer()
    n_comments = Integer()
    can_show = Boolean()
    created_at = Date()
    tags = Text(fields={'raw': Keyword()})

    class Index:
        name = 'test'

    @classmethod
    def add(cls, item):
        obj = cls(**get_item_data(item))
        obj.save()
        obj.clear_mc(item.id, item.kind)
        return obj

    @classmethod
    @cache(ITEM_MC_KEY.format('{id}', '{kind}'))
    def get(cls, id, kind):
        s = cls.search()
        s.query = Q('bool', must=[Q('term', id=id),
                                  Q('term', kind=kind)])
        rs = s.execute()
        if rs:
            return rs.hits[0]

    @classmethod
    def clear_mc(cls, id, kind):
        rdb.delete(ITEM_MC_KEY.format(id, kind))

    @classmethod
    def delete(cls, item):
        rs = cls.get(item.id, item.kind)
        if rs:
            super(cls, rs).delete()
            cls.clear_mc(item.id, item.kind)
            return True
        return False

    @classmethod
    def update_item(cls, item):
        """item是Post的ORM对象, 其实也可以放其他模型字段, 只要它们的字段都包含Item中的字段, 由kind做区分"""
        obj = cls.get(item.id, item.kind)
        if obj is None:
            return cls.add(item)
        if not obj:
            return

        kw = get_item_data(item)

        try:
            obj.update(**kw)
        except ConflictError:
            obj.clear_mc(item.id, item.kind)
            obj = cls.get(item.id, item.kind)
            obj.update(**kw)
        obj.clear_mc(item.id, item.kind)
        return True

    @classmethod
    def get_es(cls):
        search = cls.search()
        return connections.get_connection(search._using)

    @classmethod
    def bulk_update(cls, items, chunk_size=5000, op_type='update', **kwargs):
        """
        浅析ES的_source、_all、store、index: https://www.cnblogs.com/wynjauu/articles/9326168.html
        """
        index = cls._index._name
        type = cls._doc_type.name

        objects = ({
            '_op_type': op_type,
            '_id': f'{doc.id}_{doc.kind}',
            '_index': index,
            '_type': type,
            '_source': doc.to_dict()
        } for doc in items)
        client = cls.get_es()
        rs = list(parallel_bulk(client, objects,
                                chunk_size=chunk_size, **kwargs))
        for item in items:
            cls.clear_mc(item.id, item.kind)
        return rs

    @classmethod
    def new_search(cls, query, page, order_by=None, per_page=PER_PAGE):
        """用于在搜索栏搜搜, query是输入的搜索内容, 字符串"""
        s = cls.search()
        # multi_match: 多个字段匹配, SEARCH_FIELDS设置了字段权重
        s = s.query('multi_match', query=query,
                    fields=SEARCH_FIELDS)

        if page < 1:
            page = 1
        start = (page - 1) * PER_PAGE
        s = s.extra(**{'from': start, 'size': per_page})
        if order_by is not None:
            s = s.sort(order_by)
        rs = s.execute()
        dct = defaultdict(list)
        # 这里考虑了多种kind的情况, 不过我们目前只会用到Post
        for i in rs:
            dct[i.kind].append(i.id)

        items = []

        for kind, ids in dct.items():
            target_cls = TARGET_MAPPER.get(kind)
            # 最终还是依靠orm来获取数据
            if target_cls:
                items_ = target_cls.get_multi(ids)
                items.extend(items_)

        return Pagination(query, page, per_page, rs.hits.total, items)

    @classmethod
    @cache(POST_IDS_BY_TAG_MC_KEY % ('{tag}', '{page}', '{order_by}',
                                     '{per_page}'), ONE_HOUR)
    def get_post_ids_by_tag(cls, tag, page, order_by=None, per_page=PER_PAGE):
        s = cls.search()
        #s = s.query(Q('bool', must=Q('term', tags=tag)))
        s = s.query(Q('bool', must=Q('term', kind=K_POST)))
        if page < 1:
            page = 1
        start = (page - 1) * PER_PAGE
        s = s.extra(**{'from': start, 'size': per_page})
        if order_by is not None:
            if order_by == 'hot':
                s = s.query(Q('function_score', functions=[gauss_sf, score_sf]))  # noqa
            else:
                s = s.sort(order_by)
        rs = s.execute()
        ids = [obj.id for obj in rs]
        return Pagination(tag, page, per_page, rs.hits.total, ids)