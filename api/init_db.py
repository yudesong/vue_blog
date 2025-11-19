from datetime import datetime
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 导入Flask应用和数据库模型
from app import app, db
from models import User, Category, Article, Comment, Tag

# 创建应用上下文
with app.app_context():
    # 删除所有现有表并重新创建
    print("正在重置数据库...")
    db.drop_all()
    db.create_all()
    print("数据库表创建成功！")
    
    # 创建管理员用户
    print("正在创建管理员用户...")
    admin = User(
        username='admin',
        email='admin@example.com',
        password='admin123',  # 注意：在实际项目中应使用密码哈希
        avatar='https://picsum.photos/id/64/100/100',
        bio='博客管理员，热爱分享和写作。',
        is_admin=True
    )
    
    # 创建普通用户
    user1 = User(
        username='john_doe',
        email='john@example.com',
        password='password123',
        avatar='https://picsum.photos/id/237/100/100',
        bio='技术爱好者，喜欢阅读和学习新技术。'
    )
    
    user2 = User(
        username='jane_smith',
        email='jane@example.com',
        password='password456',
        avatar='https://picsum.photos/id/177/100/100',
        bio='设计师，关注用户体验和交互设计。'
    )
    
    # 添加用户到数据库
    db.session.add_all([admin, user1, user2])
    db.session.commit()
    print("用户创建成功！")
    
    # 创建分类
    print("正在创建文章分类...")
    categories = [
        Category(name='技术', description='关于编程、开发和技术趋势的文章', icon='fa-code'),
        Category(name='生活', description='关于日常生活、感悟和经验分享的文章', icon='fa-coffee'),
        Category(name='旅行', description='关于旅行经历、目的地推荐的文章', icon='fa-plane'),
        Category(name='美食', description='关于美食推荐、烹饪技巧的文章', icon='fa-cutlery'),
        Category(name='健康', description='关于健康生活、健身和营养的文章', icon='fa-heartbeat')
    ]
    
    # 添加分类到数据库
    db.session.add_all(categories)
    db.session.commit()
    print("分类创建成功！")
    
    # 创建标签
    print("正在创建文章标签...")
    tags = [
        Tag(name='Python'),
        Tag(name='Flask'),
        Tag(name='Vue.js'),
        Tag(name='前端开发'),
        Tag(name='后端开发'),
        Tag(name='全栈开发'),
        Tag(name='生活方式'),
        Tag(name='自我提升'),
        Tag(name='摄影'),
        Tag(name='读书笔记')
    ]
    
    # 添加标签到数据库
    db.session.add_all(tags)
    db.session.commit()
    print("标签创建成功！")
    
    # 创建文章
    print("正在创建示例文章...")
    articles = [
        Article(
            title='Python Flask 入门教程：构建你的第一个Web应用',
            summary='本教程将引导你使用Flask框架构建一个简单但功能完整的Web应用，适合Python初学者和想要学习Web开发的开发者。',
            content='<h2>Flask入门指南</h2><p>Flask是一个轻量级的Python Web框架，被广泛用于构建Web应用和API。本教程将从安装Flask开始，逐步引导你构建一个简单的博客应用。</p><h3>安装Flask</h3><p>首先，我们需要安装Flask。推荐使用虚拟环境来隔离项目依赖：</p><pre><code>pip install flask</code></pre><p>安装完成后，我们可以开始编写第一个Flask应用。</p><h3>第一个Flask应用</h3><p>创建一个名为app.py的文件，输入以下代码：</p><pre><code>from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)</code></pre><p>运行应用：</p><pre><code>python app.py</code></pre><p>现在，打开浏览器访问http://127.0.0.1:5000，你将看到"Hello, World!"的消息。</p>',
            cover_image='https://picsum.photos/id/1/800/400',
            status='published',
            view_count=1254,
            like_count=45,
            published_date=datetime(2023, 5, 10, 10, 30),
            author_id=admin.id,
            category_id=categories[0].id
        ),
        Article(
            title='Vue.js 3 新特性详解',
            summary='Vue.js 3带来了许多令人兴奋的新特性和性能改进，本文将详细介绍Composition API、Teleport、Fragments等重要特性。',
            content='<h2>Vue.js 3 新特性</h2><p>Vue.js 3是Vue.js框架的最新主要版本，带来了许多性能改进和新特性。本文将重点介绍一些最引人注目的变化。</p><h3>Composition API</h3><p>Composition API是Vue.js 3中最显著的新特性之一，它提供了一种更灵活的方式来组织和重用组件逻辑。</p><pre><code>&lt;script setup&gt;
import { ref, computed, onMounted } from 'vue'

const count = ref(0)
const doubled = computed(() => count.value * 2)

function increment() {
  count.value++
}

onMounted(() => {
  console.log('Component is mounted!')
})
&lt;/script&gt;

&lt;template&gt;
  &lt;button @click="increment"&gt;Count is: {{ count }}, doubled is: {{ doubled }}&lt;/button&gt;
&lt;/template&gt;</code></pre><h3>Teleport</h3><p>Teleport允许你将组件的内容渲染到DOM树中的任何位置，这对于模态框、通知等组件非常有用。</p>',
            cover_image='https://picsum.photos/id/2/800/400',
            status='published',
            view_count=987,
            like_count=32,
            published_date=datetime(2023, 6, 15, 14, 20),
            author_id=user1.id,
            category_id=categories[0].id
        ),
        Article(
            title='健康生活方式：如何保持工作与生活的平衡',
            summary='在现代快节奏的生活中，保持工作与生活的平衡变得越来越重要。本文将分享一些实用的技巧和建议，帮助你实现更好的生活平衡。',
            content='<h2>工作与生活的平衡</h2><p>在当今数字化的世界中，工作和个人生活之间的界限变得越来越模糊。许多人发现自己在工作日结束后仍然在处理工作邮件，或者在周末思考工作问题。这种不平衡可能导致压力、倦怠和健康问题。</p><h3>设定明确的界限</h3><p>实现工作与生活平衡的第一步是设定明确的界限。这可能意味着：</p><ul><li>在特定时间之后不再检查工作邮件</li><li>周末完全脱离工作</li><li>在家工作时创建专门的工作空间</li></ul><h3>优先考虑自我照顾</h3><p>照顾好自己是保持工作效率和个人幸福感的关键。确保你：</p><ul><li>获得足够的睡眠</li><li>定期锻炼</li><li>吃健康的食物</li><li>花时间做你喜欢的事情</li></ul>',
            cover_image='https://picsum.photos/id/3/800/400',
            status='published',
            view_count=1567,
            like_count=89,
            published_date=datetime(2023, 7, 2, 9, 15),
            author_id=user2.id,
            category_id=categories[4].id
        ),
        Article(
            title='探索日本京都：传统文化与现代魅力的完美结合',
            summary='京都是日本传统文化的中心，拥有众多历史悠久的神社、寺庙和传统庭院。本文将带你探索京都的必访景点和隐藏宝藏。',
            content='<h2>京都之旅</h2><p>京都是日本最具历史和文化价值的城市之一，曾作为日本的首都长达1200多年。这里保存着大量的历史建筑、传统艺术和文化遗产。</p><h3>必访景点</h3><p>在京都，有几个景点是绝对不能错过的：</p><h4>金阁寺</h4><p>金阁寺（正式名称为鹿苑寺）是京都最著名的景点之一，以其金箔覆盖的三层楼阁而闻名。这座寺庙建于1397年，是日本国宝级建筑。</p><h4>清水寺</h4><p>清水寺是京都最古老的寺庙之一，建于778年。它以其建在悬崖上的主殿和周围的樱花（春季）或红叶（秋季）而闻名。</p><h4>岚山竹林</h4><p>岚山竹林是京都最具标志性的自然景观之一，竹林小径两旁是高达30米的竹子，创造出一种神奇而宁静的氛围。</p>',
            cover_image='https://picsum.photos/id/4/800/400',
            status='published',
            view_count=2345,
            like_count=124,
            published_date=datetime(2023, 4, 18, 16, 45),
            author_id=admin.id,
            category_id=categories[2].id
        ),
        Article(
            title='在家制作完美的意式浓缩咖啡',
            summary='你不需要昂贵的专业设备就能在家制作出美味的意式浓缩咖啡。本文将分享一些简单的技巧和方法，帮助你在家中享受咖啡馆级别的咖啡。',
            content='<h2>意式浓缩咖啡入门</h2><p>意式浓缩咖啡是许多受欢迎的咖啡饮品的基础，如拿铁、卡布奇诺和摩卡。虽然专业的意式咖啡机价格昂贵，但你仍然可以使用一些简单的设备在家制作出不错的浓缩咖啡。</p><h3>所需设备</h3><p>在家制作浓缩咖啡，你需要以下设备：</p><ul><li>优质的磨豆机</li><li>法压壶或摩卡壶</li><li>电子秤（用于精确测量）</li><li>温度计（可选，但推荐）</li></ul><h3>咖啡豆选择</h3><p>选择优质的咖啡豆是制作好咖啡的关键。意式浓缩咖啡通常使用中深烘焙的咖啡豆，这种烘焙方式能够带来丰富的风味和油脂。</p><p>建议选择新鲜烘焙的咖啡豆，并在使用前现磨，以获得最佳的风味。</p>',
            cover_image='https://picsum.photos/id/5/800/400',
            status='published',
            view_count=876,
            like_count=36,
            published_date=datetime(2023, 8, 22, 11, 30),
            author_id=user1.id,
            category_id=categories[3].id
        )
    ]
    
    # 添加文章到数据库
    db.session.add_all(articles)
    db.session.commit()
    print("文章创建成功！")
    
    # 为文章添加标签
    print("正在为文章添加标签...")
    articles[0].tags.extend([tags[0], tags[1], tags[4]])  # Python, Flask, 后端开发
    articles[1].tags.extend([tags[2], tags[3], tags[5]])  # Vue.js, 前端开发, 全栈开发
    articles[2].tags.extend([tags[6], tags[7]])  # 生活方式, 自我提升
    articles[3].tags.extend([tags[8], tags[2]])  # 摄影, Vue.js
    articles[4].tags.extend([tags[6], tags[7]])  # 生活方式, 自我提升
    
    db.session.commit()
    print("标签添加成功！")
    
    # 创建评论
    print("正在创建评论...")
    comments = [
        Comment(
            content='非常感谢这篇教程！我一直想学习Flask，这篇文章让我对Flask有了很好的入门了解。',
            article_id=articles[0].id,
            author_id=user2.id,
            created_at=datetime(2023, 5, 12, 15, 20)
        ),
        Comment(
            content='我有一个问题：在实际项目中，如何处理数据库迁移？',
            article_id=articles[0].id,
            author_id=user1.id,
            created_at=datetime(2023, 5, 13, 10, 45)
        ),
        Comment(
            content='Composition API确实很棒！它让我的组件逻辑更加清晰和易于复用。',
            article_id=articles[1].id,
            author_id=admin.id,
            created_at=datetime(2023, 6, 17, 14, 10)
        ),
        Comment(
            content='这篇关于工作生活平衡的文章真的很有帮助。我一直在努力找到平衡点，这些建议非常实用。',
            article_id=articles[2].id,
            author_id=user1.id,
            created_at=datetime(2023, 7, 5, 9, 30)
        ),
        Comment(
            content='京都一直是我想去的地方。你的文章让我更加期待我的旅行了！',
            article_id=articles[3].id,
            author_id=user2.id,
            created_at=datetime(2023, 4, 20, 16, 20)
        )
    ]
    
    # 添加评论到数据库
    db.session.add_all(comments)
    db.session.commit()
    print("评论创建成功！")
    
    # 创建评论回复
    print("正在创建评论回复...")
    replies = [
        Comment(
            content='你可以使用Flask-Migrate扩展来处理数据库迁移。它基于Alembic，可以帮助你管理数据库模式的变化。',
            article_id=articles[0].id,
            author_id=admin.id,
            parent_id=comments[1].id,
            created_at=datetime(2023, 5, 13, 11, 15)
        ),
        Comment(
            content='是的，我同意。特别是对于大型组件，Composition API真的能够使代码更加组织化。',
            article_id=articles[1].id,
            author_id=user1.id,
            parent_id=comments[2].id,
            created_at=datetime(2023, 6, 18, 9, 40)
        )
    ]
    
    # 添加回复到数据库
    db.session.add_all(replies)
    db.session.commit()
    print("评论回复创建成功！")
    
    print("\n数据库初始化完成！\n")
    print("示例数据统计：")
    print(f"- 用户数量: {User.query.count()}")
    print(f"- 分类数量: {Category.query.count()}")
    print(f"- 标签数量: {Tag.query.count()}")
    print(f"- 文章数量: {Article.query.count()}")
    print(f"- 评论数量: {Comment.query.count()}")
    print(f"\n管理员账户：\n- 用户名: admin\n- 密码: admin123")