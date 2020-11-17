### Usage
初始化数据库: mysql -uroot -p  密码是: 123456
生产mysql: create database mytoutiao;
测试mysql: create database test_mytoutiao;
```
FLASK_APP=manage.py flask db init
FLASK_APP=manage.py flask db migrate
FLASK_APP=manage.py flask db upgrade
```
运行flask
```
FLASK_APP=app.py flask run
FLASK_APP=app.py FLASK_DEBUG=1 flask run
```

### 测试mysql
见test_post.py, 用idea的Run功能时, 请把`from tests.base import BaseTestCase`放在第一行, 因为base.py中会设置env=test
或用命令行:
```
env=test pytest -s
```

### 爬虫准备数据
```
python crawling.py
```

### 1. 需求

1. Post页面
2. 登陆注册(不含手机号验证码登陆)
3. 标签分类
4. 搜索
5. 点赞
6. 收藏
7. 评论
8. 用户(关注, 个人设置)
9. 热门分享/最新分享Tab
10.首页feed


### 2. 技术选型
1. flask和扩展
2. SQLALchemy
3. bootstrap
4. jquery
5. redis(键值对数据库, 缓存)
6. mysql
7. Elasticsearch(搜索)

### 3. 设计表结构(Model)

在写model的时候, 就准备好缓存
1. User
2. Contact 关注关系
3. Post
4. Like
5. Collect
6. Tag

### 4. 搭建Flask应用

### 5. 表管理(flask-migrate)

### 6. 准备数据(写爬虫): 爬RSS: https://www.dongwm.com/atom.xml

### 7. 使用Jinja2模板

### 8. 使用Bootstrap

### 9. 前端开发环境
npm install cnpm -g
cnpm i

使用webpack:
npm run start:  watch src目录的变化, 生成static/dist/*的js文件
python run.py:  watch src/templates目录的变化, 动态加载前端页面

### 10. 完成Post页面样式

### 11. 注册和登录
