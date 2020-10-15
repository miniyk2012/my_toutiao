import os

HERE = os.path.abspath(os.path.dirname(__file__))
REDIS_URL = 'redis://localhost:6379'
CACHE_REDIS_URL = REDIS_URL
DEBUG = False
SECRET_KEY = '123'
UPLOAD_FOLDER = os.path.join(HERE, 'permdir')

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root::123456@localhost/mytoutiao?charset=utf8mb4'  # noqa

PER_PAGE = 2

if not os.path.exists(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

try:
    from local_settings import *  # noqa
except ImportError:
    pass
