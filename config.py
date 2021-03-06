import os

HERE = os.path.abspath(os.path.dirname(__file__))
REDIS_URL = 'redis://localhost:6379'
CACHE_REDIS_URL = REDIS_URL
DEBUG = False
UPLOAD_FOLDER = os.path.join(HERE, 'permdir')
SQLALCHEMY_RECORD_QUERIES = True
DATABASE_QUERY_TIMEOUT = 0.5
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = '123'
SECURITY_URL_PREFIX = '/'
TEMPLATES_AUTO_RELOAD = False
SECURITY_CONFIRMABLE = True
SECURITY_REGISTERABLE = True
SECURITY_RECOVERABLE = True
SECURITY_CHANGEABLE = True
SECURITY_TRACKABLE = True
SECURITY_POST_REGISTER_VIEW = SECURITY_POST_RESET_VIEW = SECURITY_POST_CONFIRM_VIEW = 'account.landing'  # noqa
SECURITY_PASSWORD_SALT = '234'

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:12345678@localhost/mytoutiao?charset=utf8mb4'  # noqa
SQLALCHEMY_ECHO = False

SOCIAL_AUTH_USER_MODEL = 'models.user.User'
SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.weibo.WeiboOAuth2',
    'social_core.backends.douban.DoubanOAuth2',
    'social_core.backends.weixin.WeixinOAuth2'
)

SOCIAL_AUTH_GITHUB_KEY = ''
SOCIAL_AUTH_GITHUB_SECRET = ''
SOCIAL_AUTH_WEIBO_KEY = ''
SOCIAL_AUTH_WEIBO_SECRET = ''
SOCIAL_AUTH_WEIBO_DOMAIN_AS_USERNAME = True
SOCIAL_AUTH_DOUBAN_KEY = ''
SOCIAL_AUTH_DOUBAN_SECRET = ''
SOCIAL_AUTH_WEIXIN_KEY = ''
SOCIAL_AUTH_WEIXIN_SECRET = ''
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_REDIRECT_IS_HTTPS = True
CLEAN_USERNAMES = False
SOCIAL_AUTH_REMEMBER_SESSION_NAME = 'remember_me'
SOCIAL_AUTH_FIELDS_STORED_IN_SESSION = ['keep']

SECURITY_EMAIL_SUBJECT_CONFIRM = '请确认邮件 -  头条'
SECURITY_EMAIL_SUBJECT_REGISTER = '欢迎 - 头条'
SECURITY_EMAIL_SUBJECT_PASSWORD_RESET = '重置密码 - 头条'
SECURITY_EMAIL_SUBJECT_PASSWORD_CHANGE_NOTICE = '密码已改变 - 头条'
SECURITY_EMAIL_SUBJECT_PASSWORD_NOTICE = '密码已被重置 - 头条'

SECURITY_MSG_UNAUTHORIZED = ('你没有权限访问这个资源', 'error')
SECURITY_MSG_PASSWORD_MISMATCH = ('密码不匹配', 'error')
SECURITY_MSG_PASSWORD_RESET_EXPIRED = (
    ('You did not reset your password within %(within)s. '
     'New instructions have been sent to %(email)s.'), 'error')
SECURITY_MSG_DISABLED_ACCOUNT = ('账号被禁用了.', 'error')
SECURITY_MSG_INVALID_EMAIL_ADDRESS = ('邮箱地址错误', 'error')
SECURITY_MSG_PASSWORD_INVALID_LENGTH = ('错误的密码长度', 'error')
SECURITY_MSG_PASSWORD_IS_THE_SAME = ('新密码要和旧密码不一致', 'error')
SECURITY_MSG_EMAIL_NOT_PROVIDED = ('需要填写邮箱地址', 'error')
SECURITY_MSG_ALREADY_CONFIRMED = ('邮箱已经被确认', 'info')
SECURITY_MSG_PASSWORD_NOT_PROVIDED = ('需要输入密码', 'error')
SECURITY_MSG_USER_DOES_NOT_EXIST = ('用户不存在或者密码错误', 'error')
SECURITY_MSG_EMAIL_ALREADY_ASSOCIATED = ('%(email)s 已经被关联了', 'error')
SECURITY_MSG_CONFIRMATION_REQUIRED = ('登录前请先邮箱确认', 'error')
SECURITY_MSG_INVALID_PASSWORD = ('账号或者密码错误', 'error')
SECURITY_MSG_RETYPE_PASSWORD_MISMATCH = ('2次密码输入不一致', 'error')
SECURITY_USER_IDENTITY_ATTRIBUTES = ('email', 'name')

SECURITY_CONFIRM_EMAIL_WITHIN = SECURITY_RESET_PASSWORD_WITHIN = '6 hours'

CACHE_TYPE = 'redis'
FROM_USER = '812350401@qq.com'
EXMAIL_PASSWORD = 'druqkwjelztwbdjc'
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465


ES_HOSTS = ['localhost']
PER_PAGE = 2

if not os.path.exists(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

if os.getenv('env') == 'test':
    try:
        from local_settings import *  # noqa
    except ImportError:
        pass
