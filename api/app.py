from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

# 创建Flask应用实例
app = Flask(__name__)

# 配置跨域资源共享
CORS(app)

# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'blog.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
db = SQLAlchemy(app)

# 导入模型和路由
from models import Article, Category, Comment, User
from routes import article_routes, category_routes, comment_routes, auth_routes

# 注册蓝图
app.register_blueprint(article_routes, url_prefix='/api/articles')
app.register_blueprint(category_routes, url_prefix='/api/categories')
app.register_blueprint(comment_routes, url_prefix='/api/comments')
app.register_blueprint(auth_routes, url_prefix='/api/auth')

# 创建数据库表
with app.app_context():
    db.create_all()

# 根路由
@app.route('/')
def index():
    return jsonify({"message": "Welcome to InsightBlog API"})

if __name__ == '__main__':
    app.run(debug=True)