import redis

from corelib.mc import rdb


def incr_key(stat_key, amount):
    try:
        total = rdb.incr(stat_key, amount)
    except redis.exceptions.ResponseError:
        rdb.delete(stat_key)
        total = rdb.incr(stat_key, amount)
    return total
