# InsightBlog Flask API

这是InsightBlog博客应用的后台API，使用Flask框架开发，提供文章、分类、评论和用户管理等功能。

## 项目结构

```
api/
├── app.py           # 主应用文件
├── models.py        # 数据库模型定义
├── routes.py        # API路由和视图函数
├── run.py           # 应用入口点
├── .env             # 环境变量配置
├── requirements.txt # 依赖包列表
└── README.md        # 项目说明文档
```

## 功能特性

- **文章管理**：创建、查看、更新、删除文章，支持分页、搜索和筛选
- **分类管理**：创建、查看、更新、删除文章分类
- **评论管理**：创建、查看、更新、删除评论和回复
- **用户认证**：简单的登录和注册功能
- **跨域支持**：配置了CORS以支持前后端分离架构

## 技术栈

- Python 3.9+
- Flask 2.2.3
- Flask-SQLAlchemy 3.0.3
- Flask-CORS 3.0.10
- SQLite (默认) / 可选MySQL或PostgreSQL

## 安装和运行

### 1. 安装依赖

```bash
# 进入项目目录
cd /path/to/blog/api

# 使用pip安装依赖
pip install -r requirements.txt
```

### 2. 配置环境变量

编辑`.env`文件，根据需要修改配置：

```
# Flask 应用配置
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=1

# 数据库配置（默认使用SQLite）
# SQLALCHEMY_DATABASE_URI=sqlite:///blog.db

# 安全配置
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here

# 文件上传配置
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16 * 1024 * 1024  # 16MB
ALLOWED_EXTENSIONS=set(['png', 'jpg', 'jpeg', 'gif'])

# 其他配置
PER_PAGE=10
```

### 3. 运行应用

```bash
# 使用run.py运行应用
python run.py

# 或者使用Flask命令运行
flask run
```

应用将在 http://127.0.0.1:5000 启动

## API 端点

### 文章相关

- `GET /api/articles` - 获取文章列表（支持分页、筛选、搜索、排序）
- `GET /api/articles/<id>` - 获取单篇文章详情
- `POST /api/articles` - 创建新文章
- `PUT /api/articles/<id>` - 更新文章
- `DELETE /api/articles/<id>` - 删除文章
- `GET /api/articles/featured` - 获取特色文章

### 分类相关

- `GET /api/categories` - 获取分类列表
- `POST /api/categories` - 创建新分类
- `PUT /api/categories/<id>` - 更新分类
- `DELETE /api/categories/<id>` - 删除分类

### 评论相关

- `GET /api/comments` - 获取评论列表（支持分页、按文章筛选）
- `POST /api/comments` - 创建新评论
- `PUT /api/comments/<id>` - 更新评论
- `DELETE /api/comments/<id>` - 删除评论

### 认证相关

- `POST /api/auth/login` - 用户登录
- `POST /api/auth/register` - 用户注册

## 默认管理员账户

在简化的认证实现中，默认的管理员账户为：
- 用户名: `admin`
- 密码: `admin123`

> **注意**：在生产环境中，应使用更安全的认证机制，如密码哈希和JWT令牌。

## 开发注意事项

1. 本项目使用SQLite作为默认数据库，适合开发和小型应用。
2. 对于生产环境，建议使用MySQL或PostgreSQL等更强大的数据库。
3. 认证功能是简化版的，实际项目中应增强安全性。
4. 文件上传功能已在配置中设置，但具体实现需要根据需求添加。
5. 为了更好的性能，可以考虑添加缓存和优化数据库查询。

## 与前端集成

此API设计用于与Vue.js前端应用集成，特别是InsightBlog前端。确保前端应用的API调用路径与此API的端点匹配。