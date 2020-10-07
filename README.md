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

### 4. 大家Flask应用

### 5. 表管理(flask-migrate)
