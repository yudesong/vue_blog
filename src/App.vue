<template>
  <div id="app" class="min-h-screen bg-gray-50 text-gray-800 font-sans">
    <!-- 导航栏组件 - 仅在非管理页面显示 -->
    <BlogHeader 
      v-if="!isAdminView"
      :current-view="currentView"
      :is-admin-view="isAdminView"
      :is-scrolled="isScrolled"
      :current-user="currentUser"
      :is-auth-view="isAuthView"
      @switch-view="switchView"
      @switch-to-auth="switchToAuth"
      @toggle-admin-view="toggleAdminView"
      @show-user-profile="showUserProfile"
      @handle-logout="handleLogout"/>

    <!-- 主内容区 -->
    <BlogMain 
      :is-admin-view="isAdminView"
      :current-view="currentView"
      :admin-tab="adminTab"
      :is-auth-view="isAuthView"
      :current-auth-view="currentAuthView"
      :current-user="currentUser"
      :articles="articles"
      :categories="categories"
      :current-article="currentArticle"
      :related-articles="relatedArticles"
      :filtered-category="filteredCategory"
      @switch-view="switchView"
      @view-article="viewArticle"
      @filter-articles-by-category="filterArticlesByCategory"
      @clear-category-filter="clearCategoryFilter"
      @update-admin-tab="updateAdminTab"
      @show-auth-view="showAuthView"
      @switch-to-auth="switchToAuth"
      @login-success="handleLoginSuccess"
      @register-success="handleRegisterSuccess"
      @show-article-editor="showArticleEditor"
      @comment-submitted="commentSubmitted"
      @reply-submitted="replySubmitted"
      @like-toggled="likeToggled"
      @save-article="handleSaveArticle"
    />
    
    <!-- 页脚 - 仅在非管理页面显示 -->
    <BlogFooter v-if="!isAdminView" :categories="categories"/>
  </div>
</template>

<script>
import BlogHeader from './components/BlogHeader.vue'
import BlogMain from './components/BlogMain.vue'
import BlogFooter from './components/BlogFooter.vue'

export default {
  components: {
    BlogHeader,
    BlogMain,
    BlogFooter,
  },
  data() {
    return {
      // 视图状态
      isAdminView: false,
      currentView: 'home',
      mobileMenuOpen: false,
      isScrolled: false,
      adminTab: 'articles',
      // 认证相关状态
      isAuthView: false,
      currentAuthView: 'login', // 'login' 或 'register'
      currentUser: null,
      // 评论相关状态
      commentContent: '',
      isSubmittingComment: false,
      isSubmittingReply: false,
      replyBoxVisible: { visible: false, commentId: null, replyTo: null, content: '' },
      
      // 筛选状态
      filteredCategory: null,
      
      // 模态框状态
      showArticleEditor: false,
      isEditingArticle: false,
      showCategoryModal: false,
      isEditingCategory: false,
      showDeleteConfirm: false,
      deleteConfirmMessage: '',
      deleteItemId: null,
      deleteItemType: null,
      
      // 表单数据
      articleForm: {
        id: null,
        author_id: '1',
        title: '',
        category_id: '',
        tagsStr: '',
        coverImage: '',
        content: '',
        status: 'published',
        publishedDate: '',
        media: []
      },
      
      categoryForm: {
        id: null,
        name: '',
        description: '',
        icon: 'fa-file-text-o'
      },
      
      // 示例数据 - 文章
      articles: [],
      
      // 示例数据 - 分类
      categories: [],
      
      // 可用图标列表
      availableIcons: [
        'fa-code', 'fa-server', 'fa-bar-chart', 'fa-brain', 
        'fa-paint-brush', 'fa-mobile', 'fa-database', 'fa-cloud',
        'fa-file-text-o', 'fa-image', 'fa-video-camera', 'fa-music'
      ],
      
      // 当前文章
      currentArticle: null,
      
      // 相关文章
      relatedArticles: []
    }
  },
  
  computed: {
    // 特色文章
    featuredArticles() {
      return this.articles.slice(0, 3);
    },
    
    // 最新文章
    latestArticles() {
      return [...this.articles].sort((a, b) => new Date(b.publishedDate) - new Date(a.publishedDate)).slice(0, 4);
    },
    
    // 筛选后的文章
    filteredArticles() {
      if (!this.filteredCategory) {
        return this.articles;
      }
      return this.articles.filter(article => article.category === this.filteredCategory);
    },
    
    // 所有评论
    allComments() {
      let comments = [];
      if (this.articles && Array.isArray(this.articles)) {
        this.articles.forEach(article => {
          if (article.comments && Array.isArray(article.comments)) {
            article.comments.forEach(comment => {
              comments.push({...comment, articleId: article.id});
              if (comment.replies && Array.isArray(comment.replies)) {
                comment.replies.forEach(reply => {
                  comments.push({...reply, articleId: article.id, isReply: true, parentId: comment.id});
                });
              }
            });
          }
        });
      }
      return comments.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp)).slice(0, 5);
    },
    
    // 总评论数
    totalComments() {
      let count = 0;
      this.articles.forEach(article => {
        count += article.commentsCount;
      });
      return count;
    },
    
    // 总访问量
    totalViews() {
      let count = 0;
      this.articles.forEach(article => {
        count += article.views;
      });
      return count;
    }
  },
  
  created() {
    // 组件创建时初始化认证状态
    this.initAuth();
    // 页面加载时获取文章列表和分类
    this.fetchArticles();
    this.fetchCategories();
    // 监听滚动事件
    window.addEventListener('scroll', this.handleScroll);
    
    // 初始化日期
    this.articleForm.publishedDate = this.formatDateForInput(new Date());
  },
  
  beforeUnmount() {
    window.removeEventListener('scroll', this.handleScroll);
  },
  
  methods: {
    // 处理滚动事件
    handleScroll() {
      this.isScrolled = window.scrollY > 10;
    },
    
    // 切换视图
    switchView(view) {
      this.currentView = view;
      this.filteredCategory = null;
      // 滚动到顶部
      window.scrollTo(0, 0);
    },
    
    // 切换前后台视图
    toggleAdminView() {
      this.isAdminView = !this.isAdminView;
      // 滚动到顶部
      window.scrollTo(0, 0);
    },
    
    // 根据分类筛选文章
    filterArticlesByCategory(category) {
      this.filteredCategory = category;
      this.currentView = 'articles';
      // 滚动到顶部
      window.scrollTo(0, 0);
    },
    
    // 清除分类筛选
    clearCategoryFilter() {
      this.filteredCategory = null;
    },
    
    // 处理文章保存事件
    async handleSaveArticle(articleData) {
      console.log('App接收到文章保存数据:', articleData);
      
      try {
        let url = 'http://localhost:5000/api/articles';
        let method = 'POST';
        
        // 如果是更新已有文章，使用PUT方法
        if (articleData.id) {
          url += `/${articleData.id}`;
          method = 'PUT';
        } else {
          url += '/post';
        }
        
        const response = await fetch(url, {
          method: method,
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ ...articleData, author_id: '1' })
        });
        
        if (!response.ok) {
          throw new Error('Failed to save article');
        }
        
        console.log('文章保存成功，刷新数据');
        // 保存成功后重新获取文章列表，确保数据刷新
        await this.fetchArticles();
      } catch (error) {
        console.error('保存文章时出错:', error);
        alert('保存文章失败，请稍后重试');
      }
    },
    
    // API调用 - 获取文章列表
    async fetchArticles(search = '') {
      this.loading = true;
      try {
        let url = 'http://localhost:5000/api/articles';
        if (search) {
          url += `?search=${encodeURIComponent(search)}`;
        }
        
        const response = await fetch(url);
        if (!response.ok) {
          throw new Error('Failed to fetch articles');
        }
        
        var articles = await response.json();
        console.log(articles['articles']);
        this.articles = articles['articles'];
        // 简单处理热门文章（取前3篇）
        this.popularArticles = [...this.articles].slice(0, 3);
        
        // 为每篇文章添加评论计数
        for (const article of this.articles) {
          const commentsResponse = await fetch(`http://localhost:5000/api/articles/${article.id}/comments`);
          if (commentsResponse.ok) {
            const comments = await commentsResponse.json();
            article.commentsCount = comments.length;
          } else {
            article.commentsCount = 0;
          }
        }
      } catch (error) {
        console.error('Error fetching articles:', error);
        alert('获取文章失败，请稍后重试');
      } finally {
        this.loading = false;
      }
    },
    
    // API调用 - 获取分类列表
    async fetchCategories() {
      try {
        const url = 'http://localhost:5000/api/categories';
        const response = await fetch(url);
        if (!response.ok) {
          throw new Error('Failed to fetch categories');
        }
        
        this.categories = await response.json() || [];
        console.log(this.categories);
      } catch (error) {
        console.error('Error fetching categories:', error);
        // 如果API调用失败，使用本地示例数据
        this.categories = [
          { id: 1, name: '前端开发', description: '包括HTML、CSS、JavaScript等前端技术和框架相关内容', icon: 'fa-code', count: 28, lastUpdated: '2023-06-15' },
          { id: 2, name: '后端开发', description: '服务器端开发技术、数据库、API设计等相关内容', icon: 'fa-server', count: 21, lastUpdated: '2023-05-20' },
          { id: 3, name: '数据分析', description: '数据处理、分析、可视化等相关技术和工具', icon: 'fa-bar-chart', count: 15, lastUpdated: '2023-06-10' },
          { id: 4, name: '人工智能', description: '机器学习、深度学习、自然语言处理等AI相关内容', icon: 'fa-brain', count: 19, lastUpdated: '2023-05-28' },
          { id: 5, name: '设计', description: 'UI/UX设计、交互设计、视觉设计等相关内容', icon: 'fa-paint-brush', count: 12, lastUpdated: '2023-05-15' },
          { id: 6, name: '移动开发', description: 'iOS、Android应用开发相关技术和框架', icon: 'fa-mobile', count: 8, lastUpdated: '2023-05-10' }
        ];
      }
    },

    // 查看文章详情
    viewArticle(id) {
      this.currentArticle = this.articles.find(article => article.id === id);
      if (this.currentArticle) {
        // 查找相关文章（同分类，排除当前文章）
        this.relatedArticles = this.articles
          .filter(article => article.category === this.currentArticle.category && article.id !== id)
          .slice(0, 3);
        
        this.currentView = 'articleDetail';
        // 滚动到顶部
        window.scrollTo(0, 0);
      }
    },
    
    // 获取分类颜色
    getCategoryColor(category) {
      const colorMap = {
        '前端开发': 'bg-blue-500',
        '后端开发': 'bg-green-500',
        '数据分析': 'bg-yellow-500',
        '人工智能': 'bg-purple-500',
        '设计': 'bg-pink-500',
        '移动开发': 'bg-red-500'
      };
      return colorMap[category] || 'bg-gray-500';
    },
    
    // 初始化认证状态
    initAuth() {
      // 从localStorage获取用户信息
      const storedUser = localStorage.getItem('currentUser');
      if (storedUser) {
        try {
          this.currentUser = JSON.parse(storedUser);
        } catch (e) {
          console.error('Error parsing stored user:', e);
          localStorage.removeItem('currentUser');
        }
      }
    },
    
    // 显示认证视图
    showAuthView(view = 'login') {
      this.isAuthView = true;
      this.currentAuthView = view;
    },
    
    // 提交评论
    async submitComment() {
      if (!this.currentUser || !this.commentContent.trim() || this.isSubmittingComment) {
        return;
      }
      
      this.isSubmittingComment = true;
      try {
        const newComment = {
          content: this.commentContent.trim(),
          articleId: this.currentArticle.id,
          author: this.currentUser.username,
          authorAvatar: this.currentUser.avatar || 'https://picsum.photos/id/64/100/100',
          timestamp: new Date().toISOString(),
          likes: 0,
          isLiked: false,
          replies: []
        };
        
        // 尝试发送到服务器
        try {
          const response = await fetch('http://localhost:5000/api/comments', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${this.currentUser.token}`
            },
            body: JSON.stringify({
              article_id: this.currentArticle.id,
              content: newComment.content
            })
          });
          
          if (response.ok) {
            const savedComment = await response.json();
            // 合并服务器返回的数据和本地数据
            newComment.id = savedComment.id;
          }
        } catch (error) {
          console.error('Error submitting comment to server:', error);
          // 如果API调用失败，使用本地生成的ID
          newComment.id = Date.now();
        }
        
        // 更新本地数据
        if (!this.currentArticle.comments) {
          this.currentArticle.comments = [];
        }
        this.currentArticle.comments.unshift(newComment);
        this.currentArticle.commentsCount++;
        this.commentContent = '';
        
        // 显示成功通知
        this.showNotification('评论发表成功！', 'success');
      } catch (error) {
        console.error('Error submitting comment:', error);
        this.showNotification('发表评论失败，请稍后重试', 'error');
      } finally {
        this.isSubmittingComment = false;
      }
    },
    
    // 切换回复框
    toggleReplyBox(comment, replyTo = null) {
      if (this.replyBoxVisible.commentId === comment.id && !replyTo) {
        // 如果已经是当前评论的回复框，则关闭
        this.cancelReply();
      } else {
        // 打开回复框
        this.replyBoxVisible = {
          commentId: comment.id,
          replyTo: replyTo,
          content: ''
        };
      }
    },
    
    // 取消回复
    cancelReply() {
      this.replyBoxVisible = { commentId: null, replyTo: null, content: '' };
    },
    
    // 提交回复
    async submitReply(comment) {
      if (!this.currentUser || !this.replyBoxVisible.content.trim() || this.isSubmittingReply) {
        return;
      }
      
      this.isSubmittingReply = true;
      try {
        const newReply = {
          content: this.replyBoxVisible.content.trim(),
          author: this.currentUser.username,
          authorAvatar: this.currentUser.avatar || 'https://picsum.photos/id/64/100/100',
          timestamp: new Date().toISOString(),
          likes: 0,
          isLiked: false
        };
        
        // 尝试发送到服务器
        try {
          const response = await fetch('http://localhost:5000/api/comments', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${this.currentUser.token}`
            },
            body: JSON.stringify({
              article_id: this.currentArticle.id,
              content: newReply.content,
              parent_id: comment.id
            })
          });
          
          if (response.ok) {
            const savedReply = await response.json();
            // 合并服务器返回的数据
            newReply.id = savedReply.id;
          }
        } catch (error) {
          console.error('Error submitting reply to server:', error);
          // 如果API调用失败，使用本地生成的ID
          newReply.id = Date.now();
        }
        
        // 更新本地数据
        if (!comment.replies) {
          comment.replies = [];
        }
        comment.replies.push(newReply);
        this.currentArticle.commentsCount++;
        
        // 关闭回复框
        this.cancelReply();
        
        // 显示成功通知
        this.showNotification('回复发表成功！', 'success');
      } catch (error) {
        console.error('Error submitting reply:', error);
        this.showNotification('发表回复失败，请稍后重试', 'error');
      } finally {
        this.isSubmittingReply = false;
      }
    },
    
    // 点赞/取消点赞
    async toggleLike(item) {
      try {
        // 切换本地点赞状态
        item.isLiked = !item.isLiked;
        item.likes += item.isLiked ? 1 : -1;
        
        // 尝试发送到服务器
        if (this.currentUser) {
          try {
            const response = await fetch(`http://localhost:5000/api/comments/${item.id}/like`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.currentUser.token}`
              }
            });
            
            if (!response.ok) {
              // 如果服务器操作失败，恢复本地状态
              item.isLiked = !item.isLiked;
              item.likes += item.isLiked ? 1 : -1;
              throw new Error('Server operation failed');
            }
          } catch (error) {
            console.error('Error toggling like:', error);
          }
        } else {
          // 如果未登录，显示提示
          this.showNotification('请登录后再进行点赞操作', 'info');
          // 恢复本地状态
          item.isLiked = !item.isLiked;
          item.likes += item.isLiked ? 1 : -1;
        }
      } catch (error) {
        console.error('Error toggling like:', error);
      }
    },
    
    // 格式化日期
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' });
    },
    
    // 为输入框格式化日期
    formatDateForInput(date) {
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      return `${year}-${month}-${day}`;
    },
    
    // 格式化相对时间
    formatRelativeTime(timestamp) {
      const now = new Date();
      const past = new Date(timestamp);
      const diffMs = now - past;
      const diffMins = Math.floor(diffMs / (1000 * 60));
      const diffHours = Math.floor(diffMins / 60);
      const diffDays = Math.floor(diffHours / 24);
      
      if (diffMins < 1) {
        return '刚刚';
      } else if (diffMins < 60) {
        return `${diffMins}分钟前`;
      } else if (diffHours < 24) {
        return `${diffHours}小时前`;
      } else if (diffDays < 30) {
        return `${diffDays}天前`;
      } else {
        return this.formatDate(timestamp);
      }
    },
    
    // 根据ID获取文章标题
    getArticleTitleById(id) {
      const article = this.articles.find(a => a.id === id);
      return article ? article.title : '未知文章';
    },
    
    // 编辑文章
    editArticle(id) {
      const article = this.articles.find(a => a.id === id);
      if (article) {
        // 根据文章分类名称查找对应的分类ID
        const categoryId = this.categories.find(c => c.name === article.category)?.id || '';
        
        this.articleForm = {
          id: article.id,
          title: article.title,
          category_id: categoryId,
          tagsStr: article.tags.join(','),
          coverImage: article.coverImage,
          content: article.content,
          status: 'published',
          publishedDate: this.formatDateForInput(new Date(article.publishedDate)),
          media: []
        };
        this.isEditingArticle = true;
        this.showArticleEditor = true;
        
        // 将内容设置到编辑器 - 使用nextTick确保DOM完全渲染
        this.$nextTick(() => {
          if (this.$refs.editorContent) {
            this.$refs.editorContent.innerHTML = article.content || '<p></p>';
          }
        });
      }
    },
    
    // 重置文章表单
    resetArticleForm() {
      this.articleForm = {
        id: null,
        title: '',
        category_id: '',
        tagsStr: '',
        coverImage: '',
        content: '<p>开始撰写您的文章内容...</p>',
        status: 'published',
        publishedDate: this.formatDateForInput(new Date()),
        media: []
      };
      
      // 使用nextTick确保DOM渲染完成后再设置编辑器内容
      this.$nextTick(() => {
        if (this.$refs.editorContent) {
          this.$refs.editorContent.innerHTML = this.articleForm.content;
        }
      });
    },
    
    // 同步编辑器内容到articleForm
    syncEditorContent() {
      if (this.$refs.editorContent) {
        this.articleForm.content = this.$refs.editorContent.innerHTML;
      }
    },
    
    // 富文本编辑核心方法
    formatText(command, value = null) {
      // 先确保编辑器获得焦点
      if (this.$refs.editorContent) {
        this.$refs.editorContent.focus();
        
        // 尝试执行命令
        try {
          // 对于formatBlock命令，需要特殊处理
          if (command === 'formatBlock' && value) {
            document.execCommand('formatBlock', false, `<${value}>`);
          } else {
            document.execCommand(command, false, value);
          }
          this.syncEditorContent();
        } catch (error) {
          console.error('编辑器命令执行失败:', error);
        }
      }
    },
    
    // 插入链接
    insertLink() {
      const url = prompt('请输入链接地址:', 'http://');
      if (url) {
        this.formatText('createLink', url);
      }
    },
    
    // 处理封面图片上传
    handleCoverImageUpload(e) {
      const file = e.target.files[0];
      if (file) {
        // 这里只是模拟上传，实际项目中应该发送到服务器
        const reader = new FileReader();
        reader.onload = (event) => {
          this.articleForm.coverImage = event.target.result;
        };
        reader.readAsDataURL(file);
      }
    },
    
    // 触发图片上传
    triggerImageUpload() {
      document.getElementById('imageUpload').click();
    },
    
    // 触发视频上传
    triggerVideoUpload() {
      document.getElementById('videoUpload').click();
    },
    
    // 触发音频上传
    triggerAudioUpload() {
      document.getElementById('audioUpload').click();
    },
    
    // 处理图片上传
    handleImageUpload(e) {
      const file = e.target.files[0];
      if (file) {
        // 模拟上传
        const reader = new FileReader();
        reader.onload = (event) => {
          this.articleForm.media.push({
            id: Date.now(),
            type: 'image',
            url: event.target.result,
            name: file.name
          });
        };
        reader.readAsDataURL(file);
      }
      // 重置input，允许重复上传同一文件
      e.target.value = '';
    },
    
    // 处理视频上传
    handleVideoUpload(e) {
      const file = e.target.files[0];
      if (file) {
        // 模拟上传
        this.articleForm.media.push({
          id: Date.now(),
          type: 'video',
          url: '#',
          name: file.name
        });
      }
      e.target.value = '';
    },
    
    // 处理音频上传
    handleAudioUpload(e) {
      const file = e.target.files[0];
      if (file) {
        // 模拟上传
        this.articleForm.media.push({
          id: Date.now(),
          type: 'audio',
          url: '#',
          name: file.name
        });
      }
      e.target.value = '';
    },
    
    // 移除媒体
    removeMedia(id) {
      this.articleForm.media = this.articleForm.media.filter(media => media.id !== id);
    },
    
    // 更新文章
    async updateArticle() {
      alert("yudesong");
      if (!this.articleForm.id) {
        alert('请先编辑文章');
        return;
      }
      
      // 转换标签字符串为数组
      this.articleForm.tags = this.articleForm.tagsStr.split(',').map(tag => tag.trim());
      alert(this.articleForm.content);
      // 发送PUT请求更新文章
      try {
        const url = `http://localhost:5000/api/articles/${this.articleForm.id}`;
        const response = await fetch(url, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.articleForm)
        });
        
        if (!response.ok) {
          throw new Error('Failed to update article');
        }
        
        // 重置表单
        this.resetArticleForm();
        this.showArticleEditor = false;
        alert('文章更新成功');
      } catch (error) {
        console.error('Error updating article:', error);
        alert('更新文章失败，请稍后重试');
      }
    },

    // 发布文章
    async postArticle() {
      if (!this.articleForm.title.trim()) {
        alert('请输入文章标题');
        return;
      }
      if (!this.articleForm.content.trim()) {
        alert('请输入文章内容');
        return;
      }
      if (!this.articleForm.category_id) {
        alert('请选择文章分类');
        return;
      }
      
      // 转换标签字符串为数组
      this.articleForm.tags = this.articleForm.tagsStr.split(',').map(tag => tag.trim());
      
      // 发送POST请求创建文章
      try {
        const url = 'http://localhost:5000/api/articles/post';
        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ ...this.articleForm, author_id: '1' })
        });
        
        const data = await response.json();
        console.log(data)
        
        if (!response.ok) {
          throw new Error('Failed to post article');
        }
        
        // 重置表单
        this.resetArticleForm();
        this.showArticleEditor = false;
        alert('文章发布成功');
      } catch (error) {
        console.error('Error posting article:', error);
        alert('发布文章失败，请稍后重试');
      }
    },

    // 编辑分类
    editCategory(id) {
      const category = this.categories.find(c => c.id === id);
      if (category) {
        this.categoryForm = { ...category };
        this.isEditingCategory = true;
        this.showCategoryModal = true;
      }
    },
    
    // 重置分类表单
    resetCategoryForm() {
      this.categoryForm = {
        id: null,
        name: '',
        description: '',
        icon: 'fa-file-text-o'
      };
      this.isEditingCategory = false;
    },
    
    // API调用 - 更新分类
    async updateCategory() {
      if (!this.categoryForm.name.trim()) {
        alert('请输入分类名称');
        return;
      }
      
      if (!this.categoryForm.description.trim()) {
        alert('请输入分类描述');
        return;
      }
      
      try {
        const url = `http://localhost:5000/api/categories/${this.categoryForm.id}`;
        const response = await fetch(url, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.categoryForm)
        });
        
        if (!response.ok) {
          throw new Error('Failed to update category');
        }
        
        // 更新本地分类列表
        const updatedCategory = await response.json();
        const index = this.categories.findIndex(c => c.id === this.categoryForm.id);
        if (index !== -1) {
          this.categories.splice(index, 1, updatedCategory);
        }
        
        this.resetCategoryForm();
        this.showCategoryModal = false;
        alert('分类更新成功');
      } catch (error) {
        console.error('Error updating category:', error);
        alert('更新分类失败，请稍后重试');
      }
    },
    
    // API调用 - 创建分类
    async createCategory() {
      if (!this.categoryForm.name.trim()) {
        alert('请输入分类名称');
        return;
      }
      
      if (!this.categoryForm.description.trim()) {
        alert('请输入分类描述');
        return;
      }
      
      try {
        const url = 'http://localhost:5000/api/categories/create';
        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            ...this.categoryForm,
            count: 0,
            lastUpdated: new Date().toISOString().split('T')[0]
          })
        });
        
        if (!response.ok) {
          throw new Error('Failed to create category');
        }
        
        // 添加新分类到本地列表
        const newCategory = await response.json();
        this.categories.push(newCategory);
        
        this.resetCategoryForm();
        this.showCategoryModal = false;
        alert('分类创建成功');
      } catch (error) {
        console.error('Error creating category:', error);
        // 如果API调用失败，使用本地创建
        const localCategory = {
          ...this.categoryForm,
          id: Date.now(),
          count: 0,
          lastUpdated: new Date().toISOString().split('T')[0]
        };
        this.categories.push(localCategory);
        this.resetCategoryForm();
        this.showCategoryModal = false;
        alert('分类已创建（本地模式）' + error);
      }
    },
    // 删除文章
    deleteArticle(id) {
      const article = this.articles.find(a => a.id === id);
      if (article) {
        this.deleteItemId = id;
        this.deleteItemType = 'article';
        this.deleteConfirmMessage = `确定要删除文章《${article.title}》吗？此操作不可撤销。`;
        this.showDeleteConfirm = true;
      }
    },
    
    // 删除分类
    deleteCategory(id) {
      const category = this.categories.find(c => c.id === id);
      if (category) {
        this.deleteItemId = id;
        this.deleteItemType = 'category';
        this.deleteConfirmMessage = `确定要删除分类《${category.name}》吗？该分类下的${category.count}篇文章将受到影响。`;
        this.showDeleteConfirm = true;
      }
    },
    
    // 认证相关方法
    switchToAuth(view) {
      this.isAuthView = true;
      this.currentAuthView = view;
      this.mobileMenuOpen = false;
      // 滚动到页面顶部
      window.scrollTo({ top: 0, behavior: 'smooth' });
    },
    
    handleLoginSuccess(user) {
      // 保存用户信息到本地存储
      localStorage.setItem('currentUser', JSON.stringify(user));
      this.currentUser = user;
      this.isAuthView = false;
      this.currentView = 'home';
      
      // 显示成功消息
      this.showNotification('登录成功！', 'success');
    },
    
    handleRegisterSuccess() {
      // 注册成功后切换到登录页面
      this.currentAuthView = 'login';
      this.showNotification('注册成功，请登录！', 'success');
    },
    
    handleLogout() {
      // 清除本地存储的用户信息
      localStorage.removeItem('currentUser');
      this.currentUser = null;
      this.isAuthView = false;
      this.currentView = 'home';
      
      // 如果在管理后台视图，切换到前台
      if (this.isAdminView) {
        this.isAdminView = false;
      }
      
      this.showNotification('已成功退出登录', 'success');
    },
    
    showUserProfile() {
      // 这里可以实现显示用户资料的逻辑
      this.mobileMenuOpen = false;
      // 目前简单切换到首页
      this.switchView('home');
      this.showNotification('用户资料功能正在开发中...', 'info');
    },
    
    checkUserLoginStatus() {
      // 从本地存储检查用户登录状态
      const savedUser = localStorage.getItem('currentUser');
      if (savedUser) {
        try {
          this.currentUser = JSON.parse(savedUser);
        } catch (e) {
          console.error('解析用户信息失败:', e);
          localStorage.removeItem('currentUser');
        }
      }
    },
    
    showNotification(message, type = 'info') {
      // 简单的通知提示函数
      const notification = document.createElement('div');
      notification.className = `fixed bottom-4 right-4 px-6 py-3 rounded-md shadow-lg z-50 transition-all duration-300 transform translate-y-0`;
      
      // 根据类型设置样式
      if (type === 'success') {
        notification.classList.add('bg-green-500', 'text-white');
      } else if (type === 'error') {
        notification.classList.add('bg-red-500', 'text-white');
      } else if (type === 'warning') {
        notification.classList.add('bg-yellow-500', 'text-white');
      } else {
        notification.classList.add('bg-blue-500', 'text-white');
      }
      
      notification.textContent = message;
      document.body.appendChild(notification);
      
      // 3秒后移除通知
      setTimeout(() => {
        notification.classList.add('opacity-0', 'translate-y-4');
        setTimeout(() => {
          document.body.removeChild(notification);
        }, 300);
      }, 3000);
    },
    
    // 初始化函数 - 在组件挂载时调用
    //initAuth() {
      // 检查本地存储中的用户信息
      //this.checkUserLoginStatus();
    //},
    
    // 确认删除
    async confirmDelete() {
      try {
        if (this.deleteItemType === 'article') {
          // 调用API删除文章
          const url = `http://localhost:5000/api/articles/${this.deleteItemId}`;
          const response = await fetch(url, {
            method: 'DELETE',
            headers: {
              'Content-Type': 'application/json'
            }
          });
          
          if (!response.ok) {
            throw new Error('Failed to delete article');
          }
          
          // 更新本地数据
          this.articles = this.articles.filter(a => a.id !== this.deleteItemId);
          alert('文章删除成功');
        } else if (this.deleteItemType === 'category') {
          this.categories = this.categories.filter(c => c.id !== this.deleteItemId);
        }
      } catch (error) {
        console.error(`Error deleting ${this.deleteItemType}:`, error);
        alert(`删除${this.deleteItemType === 'article' ? '文章' : '分类'}失败，请稍后重试`);
      } finally {
        this.showDeleteConfirm = false;
      }
    },  
    
    // 生命周期钩子 - 组件挂载时
    mounted() {
      // 初始化认证状态
      this.initAuth();
    }
  }
}
</script>

<style>

@import '@fortawesome/fontawesome-free/css/all.css';

/* 全局样式 */
#app {
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
}

/* 自定义动画 */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-fadeIn {
  animation: fadeIn 0.3s ease-out forwards;
}

/* 文章内容样式 */
.article-content h2 {
  font-size: 1.5rem;
  font-weight: bold;
  margin-top: 1.5rem;
  margin-bottom: 1rem;
  color: #1a202c;
}

.article-content h3 {
  font-size: 1.25rem;
  font-weight: bold;
  margin-top: 1.25rem;
  margin-bottom: 0.75rem;
  color: #1a202c;
}

.article-content p {
  margin-bottom: 1rem;
  line-height: 1.6;
}

.article-content ul {
  margin-bottom: 1rem;
  padding-left: 1.5rem;
  list-style-type: disc;
}

.article-content li {
  margin-bottom: 0.5rem;
}

.article-content pre {
  background-color: #f7fafc;
  padding: 1rem;
  border-radius: 0.375rem;
  overflow-x: auto;
  margin-bottom: 1rem;
}

.article-content code {
  font-family: 'Fira Code', monospace;
  font-size: 0.875rem;
}

/* 评论区域样式 */
.article-comments {
  margin-top: 2rem;
}

.comment-item {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
  background-color: #ffffff;
  border: 1px solid #f1f1f1;
}

.comment-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.comment-author-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.comment-content {
  background-color: #f9fafb;
  border-radius: 8px;
  padding: 0.75rem 1rem;
  font-size: 0.95rem;
  line-height: 1.6;
  color: #374151;
}

.comment-actions {
  margin-top: 0.5rem;
}

.comment-actions button {
  transition: all 0.2s ease;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  border: none;
  background: none;
  cursor: pointer;
}

.comment-actions button:hover {
  background-color: #f3f4f6;
}

.comment-like-btn i {
  transition: color 0.2s ease;
}

.comment-like-btn:hover i {
  color: #f87171;
  transform: scale(1.1);
}

.comment-like-btn.active i {
  color: #f87171;
}

.comment-reply-btn:hover {
  text-decoration: underline;
  color: #4f46e5;
}

.reply-item {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  margin-left: 1.5rem;
  border-radius: 8px;
  padding: 0.75rem;
  background-color: #f9fafb;
  border: 1px solid #f1f1f1;
}

.reply-item:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.reply-author-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
}

.reply-content {
  font-size: 0.875rem;
  line-height: 1.5;
  color: #374151;
}

.comment-form textarea,
.reply-form textarea {
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
  font-family: inherit;
  font-size: 0.95rem;
  resize: vertical;
  min-height: 80px;
}

.comment-form textarea:focus,
.reply-form textarea:focus {
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.comment-form textarea:disabled,
.reply-form textarea:disabled {
  background-color: #f9fafb;
  cursor: not-allowed;
  opacity: 0.7;
}

.btn-primary {
  transition: all 0.2s ease;
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(79, 70, 229, 0.2);
}

.btn-primary:active {
  transform: translateY(0);
}

.btn-secondary {
  transition: all 0.2s ease;
}

.btn-secondary:hover {
  background-color: #f3f4f6;
}

.not-logged-in-notice {
  text-align: center;
  padding: 1.5rem;
  background-color: #fef3c7;
  border: 1px solid #fcd34d;
  border-radius: 8px;
  color: #92400e;
  font-size: 0.95rem;
}
</style>
