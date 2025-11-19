from flask import Blueprint, jsonify, request
from models import Article, Category, Comment, User, Tag, db
from datetime import datetime

# 创建蓝图
article_routes = Blueprint('article_routes', __name__)
category_routes = Blueprint('category_routes', __name__)
comment_routes = Blueprint('comment_routes', __name__)
auth_routes = Blueprint('auth_routes', __name__)

# 文章相关路由
@article_routes.route('/', methods=['GET'])
def get_articles():
    # 获取查询参数
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    category = request.args.get('category')
    status = request.args.get('status')
    search = request.args.get('search')
    sort_by = request.args.get('sort_by', 'published_date')
    sort_order = request.args.get('sort_order', 'desc')
    
    # 构建查询
    query = Article.query
    
    if category:
        query = query.join(Category).filter(Category.name == category)
    
    if status:
        query = query.filter(Article.status == status)
    
    if search:
        search = f"%{search}%"
        query = query.filter(
            Article.title.like(search) | 
            Article.summary.like(search) | 
            Article.content.like(search)
        )
    
    # 排序
    if sort_order == 'desc':
        query = query.order_by(getattr(Article, sort_by).desc())
    else:
        query = query.order_by(getattr(Article, sort_by))
    
    # 分页
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    # 格式化文章数据
    articles = []
    for article in pagination.items:
        article_data = {
            'id': article.id,
            'title': article.title,
            'summary': article.summary,
            'content': article.content,
            'coverImage': article.cover_image,
            'status': article.status,
            'views': article.view_count,
            'likes': article.like_count,
            'publishedDate': article.published_date.isoformat() if article.published_date else None,
            'author': {
                # 'id': article.author.id,
                # 'username': article.author.username,
                # 'avatar': article.author.avatar
            },
            'category': article.category_rel.name if article.category_rel else None,
            'commentsCount': len(article.comments),
            'tags': [tag.name for tag in article.tags]
        }
        articles.append(article_data)
    print(articles)
    # 返回分页数据
    return jsonify({
        'articles': articles,
        'total': pagination.total,
        'page': pagination.page,
        'pages': pagination.pages,
        'perPage': pagination.per_page,
        'hasNext': pagination.has_next,
        'hasPrev': pagination.has_prev
    })

@article_routes.route('/<int:article_id>', methods=['GET'])
def get_article(article_id):
    article = Article.query.get_or_404(article_id)
    
    # 增加浏览量
    article.view_count += 1
    db.session.commit()
    
    # 格式化文章数据
    article_data = {
        'id': article.id,
        'title': article.title,
        'summary': article.summary,
        'content': article.content,
        'coverImage': article.cover_image,
        'status': article.status,
        'views': article.view_count,
        'likes': article.like_count,
        'publishedDate': article.published_date.isoformat() if article.published_date else None,
        'author': {
            'id': article.author.id,
            'username': article.author.username,
            'avatar': article.author.avatar,
            'bio': article.author.bio
        },
        'category': article.category_rel.name if article.category_rel else None,
        'categoryColor': '#6366F1' if article.category_rel else None,  # 默认颜色
        'comments': [{
            'id': comment.id,
            'content': comment.content,
            'likes': comment.like_count,
            'timestamp': comment.created_at.isoformat(),
            'author': {
                'id': comment.author.id,
                'username': comment.author.username,
                'avatar': comment.author.avatar
            },
            'replies': [{
                'id': reply.id,
                'content': reply.content,
                'likes': reply.like_count,
                'timestamp': reply.created_at.isoformat(),
                'author': {
                    'id': reply.author.id,
                    'username': reply.author.username,
                    'avatar': reply.author.avatar
                }
            } for reply in comment.replies]
        } for comment in article.comments],
        'commentsCount': len(article.comments),
        'tags': [tag.name for tag in article.tags]
    }
    
    return jsonify(article_data)

@article_routes.route('/post', methods=['POST'])
def create_article():
    data = request.json
    print(data)
    # 验证必需字段
    required_fields = ['title', 'content', 'author_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    # 创建新文章
    new_article = Article(
        title=data['title'],
        summary=data.get('summary', ''),
        content=data['content'],
        cover_image=data.get('coverImage', 'https://picsum.photos/id/1073/800/400'),
        status=data.get('status', 'draft'),
        author_id=data['author_id']
    )
    
    # 处理分类
    if 'category_id' in data:
        new_article.category_id = data['category_id']
    
    # 处理标签
    if 'tags' in data:
        for tag_name in data['tags']:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.session.add(tag)
            new_article.tags.append(tag)
    
    # 处理发布日期
    if data.get('status') == 'published' and 'publishedDate' in data:
        # 处理带Z后缀的ISO格式日期
        published_date_str = data['publishedDate']
        # 移除末尾的Z字符（如果存在）
        if published_date_str.endswith('Z'):
            published_date_str = published_date_str[:-1]
        new_article.published_date = datetime.fromisoformat(published_date_str)
    
    # 保存到数据库
    db.session.add(new_article)
    db.session.commit()
    
    return jsonify({'id': new_article.id}), 201

@article_routes.route('/<int:article_id>', methods=['PUT'])
def update_article(article_id):
    article = Article.query.get_or_404(article_id)
    data = request.json
    
    # 更新字段
    if 'title' in data:
        article.title = data['title']
    if 'summary' in data:
        article.summary = data['summary']
    if 'content' in data:
        article.content = data['content']
    if 'coverImage' in data:
        article.cover_image = data['coverImage']
    if 'status' in data:
        article.status = data['status']
    if 'category_id' in data:
        article.category_id = data['category_id']
    if 'publishedDate' in data:
        # 处理带Z后缀的ISO格式日期
        published_date_str = data['publishedDate']
        # 移除末尾的Z字符（如果存在）
        if published_date_str.endswith('Z'):
            published_date_str = published_date_str[:-1]
        article.published_date = datetime.fromisoformat(published_date_str)
    
    # 处理标签
    if 'tags' in data:
        # 清除现有标签
        article.tags = []
        for tag_name in data['tags']:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.session.add(tag)
            article.tags.append(tag)
    
    # 保存到数据库
    db.session.commit()
    
    return jsonify({'message': 'Article updated successfully'})

@article_routes.route('/<int:article_id>', methods=['DELETE'])
def delete_article(article_id):
    article = Article.query.get_or_404(article_id)
    
    # 删除文章
    db.session.delete(article)
    db.session.commit()
    
    return jsonify({'message': 'Article deleted successfully'})

@article_routes.route('/featured', methods=['GET'])
def get_featured_articles():
    # 获取特色文章（前3篇已发布的文章）
    articles = Article.query.filter_by(status='published').order_by(Article.published_date.desc()).limit(3).all()
    
    # 格式化文章数据
    featured_articles = []
    for article in articles:
        article_data = {
            'id': article.id,
            'title': article.title,
            'summary': article.summary,
            'coverImage': article.cover_image,
            'publishedDate': article.published_date.isoformat() if article.published_date else None,
            'author': {
                'id': article.author.id,
                'username': article.author.username,
                'avatar': article.author.avatar
            },
            'category': article.category_rel.name if article.category_rel else None,
            'commentsCount': len(article.comments),
            'views': article.view_count
        }
        featured_articles.append(article_data)
    
    return jsonify(featured_articles)

# 分类相关路由
@category_routes.route('/', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    
    # 格式化分类数据
    category_list = []
    for category in categories:
        category_data = {
            'id': category.id,
            'name': category.name,
            'description': category.description,
            'icon': category.icon,
            'count': len(category.articles),
            'lastUpdated': max([article.updated_at for article in category.articles], default=category.updated_at).isoformat() if category.articles else category.updated_at.isoformat()
        }
        category_list.append(category_data)
    
    return jsonify(category_list)

@category_routes.route('/create', methods=['POST'])
def create_category():
    data = request.json
    print(data)

    # 验证必需字段
    if 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    
    # 检查分类是否已存在
    if Category.query.filter_by(name=data['name']).first():
        return jsonify({'error': 'Category already exists'}), 400
    
    # 创建新分类
    new_category = Category(
        name=data['name'],
        description=data.get('description', ''),
        icon=data.get('icon', 'fa-folder')
    )
    
    # 保存到数据库
    db.session.add(new_category)
    db.session.commit()
    
    return jsonify({'id': new_category.id}), 201

@category_routes.route('/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    category = Category.query.get_or_404(category_id)
    data = request.json
    
    # 更新字段
    if 'name' in data:
        # 检查新名称是否已存在
        existing_category = Category.query.filter_by(name=data['name']).first()
        if existing_category and existing_category.id != category_id:
            return jsonify({'error': 'Category name already exists'}), 400
        category.name = data['name']
    if 'description' in data:
        category.description = data['description']
    if 'icon' in data:
        category.icon = data['icon']
    
    # 保存到数据库
    db.session.commit()
    
    return jsonify({'message': 'Category updated successfully'})

@category_routes.route('/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    
    # 删除分类（会自动处理相关的文章关系）
    db.session.delete(category)
    db.session.commit()
    
    return jsonify({'message': 'Category deleted successfully'})

# 评论相关路由
@comment_routes.route('/', methods=['GET'])
def get_comments():
    # 获取查询参数
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    article_id = request.args.get('article_id', type=int)
    
    # 构建查询
    query = Comment.query
    
    if article_id:
        query = query.filter(Comment.article_id == article_id)
    
    # 按创建时间降序排序
    query = query.order_by(Comment.created_at.desc())
    
    # 分页
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    # 格式化评论数据
    comments = []
    for comment in pagination.items:
        # 只获取顶级评论（非回复）
        if not comment.parent_id:
            comment_data = {
                'id': comment.id,
                'content': comment.content,
                'likes': comment.like_count,
                'timestamp': comment.created_at.isoformat(),
                'articleId': comment.article_id,
                'author': {
                    'id': comment.author.id,
                    'username': comment.author.username,
                    'avatar': comment.author.avatar
                },
                'replies': [{
                    'id': reply.id,
                    'content': reply.content,
                    'likes': reply.like_count,
                    'timestamp': reply.created_at.isoformat(),
                    'author': {
                        'id': reply.author.id,
                        'username': reply.author.username,
                        'avatar': reply.author.avatar
                    }
                } for reply in comment.replies]
            }
            comments.append(comment_data)
    
    # 返回分页数据
    return jsonify({
        'comments': comments,
        'total': pagination.total,
        'page': pagination.page,
        'pages': pagination.pages,
        'perPage': pagination.per_page,
        'hasNext': pagination.has_next,
        'hasPrev': pagination.has_prev
    })

@comment_routes.route('/', methods=['POST'])
def create_comment():
    data = request.json
    
    # 验证必需字段
    required_fields = ['content', 'article_id', 'author_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    # 创建新评论
    new_comment = Comment(
        content=data['content'],
        article_id=data['article_id'],
        author_id=data['author_id'],
        parent_id=data.get('parent_id')
    )
    
    # 保存到数据库
    db.session.add(new_comment)
    db.session.commit()
    
    return jsonify({'id': new_comment.id}), 201

@comment_routes.route('/<int:comment_id>', methods=['PUT'])
def update_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    data = request.json
    
    # 更新字段
    if 'content' in data:
        comment.content = data['content']
    
    # 保存到数据库
    db.session.commit()
    
    return jsonify({'message': 'Comment updated successfully'})

@comment_routes.route('/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    
    # 删除评论
    db.session.delete(comment)
    db.session.commit()
    
    return jsonify({'message': 'Comment deleted successfully'})

# 认证相关路由（简化版）
@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.json
    
    # 简化的登录逻辑，实际项目中应该使用密码哈希等安全措施
    if data.get('username') == 'admin' and data.get('password') == 'admin123':
        # 在实际项目中，这里应该生成JWT token
        return jsonify({
            'id': 1,
            'username': 'admin',
            'email': 'admin@example.com',
            'avatar': 'https://picsum.photos/id/64/100/100',
            'isAdmin': True,
            'token': 'mock-jwt-token'
        })
    
    return jsonify({'error': 'Invalid credentials'}), 401

@auth_routes.route('/register', methods=['POST'])
def register():
    data = request.json
    
    # 验证必需字段
    required_fields = ['username', 'email', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    # 检查用户名和邮箱是否已存在
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    # 创建新用户（简化版，实际项目中应该使用密码哈希）
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=data['password']  # 实际项目中应该使用密码哈希
    )
    
    # 保存到数据库
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'id': new_user.id}), 201