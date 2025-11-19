<template>
  <div v-if="article" class="bg-white rounded-lg shadow-sm p-6 animate-fadeIn">
    <!-- 文章头部信息 -->
    <div class="mb-6">
      <div class="flex items-center space-x-2 mb-3">
        <span 
          :class="['inline-block px-2 py-1 text-xs font-medium rounded', getCategoryColor(article.category)]"
          style="background-color: var(--category-color, #4299e1);"
        >
          {{ article.category }}
        </span>
        <span class="text-gray-500 text-sm">{{ formatDate(article.publishedDate) }}</span>
      </div>
      <h1 class="text-3xl font-bold mb-4 text-gray-800">{{ article.title }}</h1>
      
      <!-- 标签 -->
      <div class="flex flex-wrap gap-2 mb-4">
        <span 
          v-for="tag in article.tags" 
          :key="tag"
          class="inline-block px-3 py-1 bg-gray-100 text-gray-600 text-sm rounded-full"
        >
          {{ tag }}
        </span>
      </div>
    </div>
    
    <!-- 文章封面图 -->
    <div v-if="article.coverImage" class="mb-8">
      <img 
        :src="article.coverImage" 
        :alt="article.title" 
        class="w-full h-auto rounded-lg object-cover max-h-96 object-center"
      />
    </div>
    
    <!-- 文章内容 -->
    <div class="article-content mb-8 text-gray-700" v-html="article.content"></div>
    
    <!-- 文章交互区 -->
    <div class="flex justify-between items-center py-4 border-t border-b border-gray-100 mb-8">
      <div class="flex items-center space-x-4">
        <button class="flex items-center text-gray-500 hover:text-blue-600 transition-colors">
          <i class="fa fa-thumbs-up mr-1"></i>
          <span>{{ article.likes }}</span>
        </button>
        <button class="flex items-center text-gray-500 hover:text-blue-600 transition-colors">
          <i class="fa fa-bookmark mr-1"></i>
          <span>{{ article.saves || 0 }}</span>
        </button>
        <button class="flex items-center text-gray-500 hover:text-blue-600 transition-colors">
          <i class="fa fa-share-alt mr-1"></i>
          <span>分享</span>
        </button>
      </div>
      <div class="flex items-center text-gray-500 text-sm">
        <i class="fa fa-eye mr-1"></i>
        <span>{{ article.views }} 次浏览</span>
      </div>
    </div>
    
    <!-- 作者信息 -->
    <div class="flex items-center p-4 bg-gray-50 rounded-lg mb-8">
      <img :src="article.authorAvatar" :alt="article.author" class="w-12 h-12 rounded-full mr-4" />
      <div>
        <h3 class="font-medium text-gray-800 mb-1">{{ article.author }}</h3>
        <p class="text-gray-600 text-sm mb-1">{{ article.authorBio }}</p>
        <button class="text-blue-600 text-sm hover:underline">关注作者</button>
      </div>
    </div>
    
    <!-- 评论区 -->
    <div class="mb-8">
      <h3 class="text-xl font-bold mb-4 text-gray-800">评论 ({{ article.commentsCount || article.comments?.length || 0 }})</h3>
      
      <!-- 评论输入框 -->
      <div class="bg-gray-50 p-4 rounded-lg mb-6">
        <div class="flex space-x-3">
          <div v-if="!isLoggedIn" class="w-full bg-white p-4 rounded text-center mb-4">
            <p class="text-gray-600">请先登录后再发表评论</p>
            <button @click="$parent.switchToAuth && $parent.switchToAuth('login')" class="mt-2 px-4 py-1 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors">登录</button>
          </div>
          <img v-else src="https://picsum.photos/id/1005/100/100" alt="Your avatar" class="w-10 h-10 rounded-full" />
          <div class="flex-1">
            <textarea 
              v-model="newComment"
              placeholder="写下您的评论..."
              class="w-full p-3 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
              rows="3"
              :disabled="!isLoggedIn || isLoading"
            ></textarea>
            <div class="flex justify-end mt-2">
              <button 
                @click="submitComment"
                :disabled="!isLoggedIn || !newComment.trim() || isLoading"
                class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors disabled:opacity-50"
              >
                <span v-if="!isLoading">发表评论</span>
                <span v-else>提交中...</span>
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 评论列表 -->
      <div v-if="article.comments && article.comments.length > 0" class="space-y-4">
        <div v-for="comment in article.comments" :key="comment.id" class="bg-white p-4 rounded-lg border border-gray-100">
          <div class="flex space-x-3">
            <img :src="comment.avatar" :alt="comment.author" class="w-10 h-10 rounded-full" />
            <div class="flex-1">
              <div class="flex items-center justify-between mb-1">
                <div class="font-medium text-gray-800">{{ comment.author }}</div>
                <div class="text-gray-400 text-xs">{{ formatDate(comment.timestamp) }}</div>
              </div>
              <p class="text-gray-600 mb-2">{{ comment.content }}</p>
              <div class="flex items-center text-gray-500 text-sm space-x-3">
                <button @click="toggleLike(comment)" class="hover:text-red-500 transition-colors">
                  <i class="fa fa-thumbs-up mr-1"></i>
                  <span>{{ comment.likes || 0 }}</span>
                </button>
                <button class="hover:text-blue-600 transition-colors" @click="toggleReplyBox(comment.id)">
                  <i class="fa fa-reply mr-1"></i>
                  <span>回复</span>
                </button>
              </div>
              
              <!-- 回复框 -->
              <div v-if="replyingTo === comment.id" class="mt-3 p-3 bg-gray-50 rounded-lg">
                <textarea 
                  v-model="replyContent"
                  :placeholder="`回复${replyTarget ? ' ' + replyTarget : ''}...`"
                  class="w-full p-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-300 transition-all"
                  rows="2"
                ></textarea>
                <div class="flex justify-end mt-2 space-x-2">
                  <button 
                    @click="cancelReply"
                    class="px-3 py-1 text-gray-600 bg-gray-200 rounded hover:bg-gray-300 transition-colors"
                  >
                    取消
                  </button>
                  <button 
                    @click="submitReply(comment.id)"
                    :disabled="!replyContent.trim()"
                    class="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors disabled:opacity-50"
                  >
                    回复
                  </button>
                </div>
              </div>
              
              <!-- 回复列表 -->
              <div v-if="comment.replies && comment.replies.length > 0" class="mt-3 space-y-3 pl-4 border-l-2 border-gray-100">
                <div v-for="reply in comment.replies" :key="reply.id" class="p-3 bg-gray-50 rounded-lg">
                  <div class="flex items-center justify-between mb-1">
                    <div class="font-medium text-gray-800 text-sm">{{ reply.author }}</div>
                    <div class="text-gray-400 text-xs">{{ formatDate(reply.timestamp) }}</div>
                  </div>
                  <p class="text-gray-600 text-sm">
                    <span class="text-blue-600">@{{ reply.replyTo }}</span> {{ reply.content }}
                  </p>
                  <div class="flex items-center text-gray-500 text-xs space-x-3 mt-1">
                    <button @click="toggleLike(reply)" class="hover:text-red-500 transition-colors">
                      <i class="fa fa-thumbs-up mr-1"></i>
                      <span>{{ reply.likes || 0 }}</span>
                    </button>
                    <button @click="toggleReplyBox(comment.id, reply.author)" class="hover:text-blue-600 transition-colors">
                      <span>回复</span>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 无评论提示 -->
      <div v-else class="text-center py-8 text-gray-500 bg-gray-50 rounded-lg">
        <i class="fa fa-comment-slash text-3xl mb-2"></i>
        <p>暂无评论，来发表第一条评论吧！</p>
      </div>
    </div>
    
    <!-- 相关文章 -->
    <div v-if="relatedArticles && relatedArticles.length > 0" class="mb-8">
      <h3 class="text-xl font-bold mb-4 text-gray-800">相关文章</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div v-for="relatedArticle in relatedArticles" :key="relatedArticle.id" class="bg-white rounded-lg shadow-sm overflow-hidden hover:shadow-md transition-shadow">
          <div class="h-32 overflow-hidden">
            <img 
              :src="relatedArticle.coverImage" 
              :alt="relatedArticle.title" 
              class="w-full h-full object-cover transition-transform hover:scale-105"
            />
          </div>
          <div class="p-3">
            <h4 class="font-medium text-gray-800 mb-1 line-clamp-2 hover:text-blue-600 transition-colors cursor-pointer" @click="viewArticle(relatedArticle.id)">
              {{ relatedArticle.title }}
            </h4>
            <div class="flex items-center text-gray-500 text-xs">
              <span>{{ formatDate(relatedArticle.publishedDate) }}</span>
              <span class="mx-2">·</span>
              <span>{{ relatedArticle.views }} 浏览</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  
  <!-- 文章未找到提示 -->
  <div v-else class="bg-white rounded-lg shadow-sm p-8 text-center text-gray-500 animate-fadeIn">
    <i class="fa fa-search text-4xl mb-3"></i>
    <h3 class="text-xl font-bold mb-2">文章未找到</h3>
    <p>您请求的文章不存在或已被删除。</p>
  </div>
</template>

<script>
import hljs from 'highlight.js';
import 'highlight.js/styles/atom-one-dark.css';

export default {
  name: 'ArticleDetail',
  props: {
    article: {
      type: Object,
      required: true
    },
    relatedArticles: {
      type: Array,
      default: () => []
    }
  },
  data() {
      return {
        newComment: '',
        replyContent: '',
        replyingTo: null,
        replyTarget: null,
        isLoading: false,
        isLoggedIn: false,
        currentUser: null
      }
    },
    
    created() {
      // 初始化用户登录状态
      this.initAuth();
    },
    
    mounted() {
    // 应用代码高亮并添加复制按钮
    this.highlightCodeWithCopyButtons();
  },
  
  updated() {
    // 当组件更新时，只需要重新高亮代码，避免重复添加复制按钮
    const codeBlocks = document.querySelectorAll('.article-content pre code');
    codeBlocks.forEach(block => {
      // 只重新高亮代码内容，不添加复制按钮
      hljs.highlightElement(block);
    });
  },
    
    methods: {
      // 初始化认证状态
      initAuth() {
        // 从localStorage获取用户信息
        const userStr = localStorage.getItem('currentUser');
        if (userStr) {
          try {
            this.currentUser = JSON.parse(userStr);
            this.isLoggedIn = true;
          } catch (e) {
            console.error('解析用户信息失败:', e);
            localStorage.removeItem('currentUser');
          }
        }
        
        // 监听父组件的用户状态变化
        if (this.$parent && this.$parent.currentUser) {
          this.currentUser = this.$parent.currentUser;
          this.isLoggedIn = !!this.$parent.currentUser;
        }
      },
      
      // 格式化日期显示
      formatDate(dateString) {
        if (!dateString) return '';
        const date = new Date(dateString);
        const now = new Date();
        const diffMs = now - date;
        const diffMins = Math.floor(diffMs / 60000);
        const diffHours = Math.floor(diffMs / 3600000);
        const diffDays = Math.floor(diffMs / 86400000);
        
        if (diffMins < 1) return '刚刚';
        if (diffMins < 60) return `${diffMins}分钟前`;
        if (diffHours < 24) return `${diffHours}小时前`;
        if (diffDays < 7) return `${diffDays}天前`;
        
        return date.toLocaleDateString('zh-CN');
      },
      
      // 应用代码高亮并添加复制按钮
    highlightCodeWithCopyButtons() {
      const codeBlocks = document.querySelectorAll('.article-content pre code');
      codeBlocks.forEach(block => {
        // 先应用高亮
        hljs.highlightElement(block);
        
        // 为代码块添加复制按钮
        this.addCopyButtonToBlock(block);
      });
    },
    
    // 为代码块添加复制按钮（单独方法便于管理）
    addCopyButtonToBlock(block) {
      const preElement = block.parentElement;
      // 检查是否已经有复制按钮，避免重复添加
      if (preElement && !preElement.querySelector('.copy-button')) {
        // 创建复制按钮
        const copyButton = document.createElement('button');
        copyButton.className = 'copy-button';
        copyButton.innerHTML = '<i class="fa fa-copy"></i>';
        copyButton.title = '复制代码';
        copyButton.addEventListener('click', (e) => {
          e.stopPropagation();
          this.copyCode(block.textContent);
          // 临时更改按钮文本为"已复制"
          const originalText = copyButton.innerHTML;
          copyButton.innerHTML = '<i class="fa fa-check"></i>';
          setTimeout(() => {
            copyButton.innerHTML = originalText;
          }, 2000);
        });
        
        // 确保pre元素有相对定位
        if (window.getComputedStyle(preElement).position === 'static') {
          preElement.style.position = 'relative';
        }
        
        // 添加按钮到pre元素
        preElement.appendChild(copyButton);
      }
    },
      
      // 复制代码功能
        copyCode(text) {
          navigator.clipboard.writeText(text).then(() => {
            // 使用现有的showNotification方法显示成功消息
            this.showNotification('代码已复制到剪贴板');
          }).catch(err => {
            console.error('复制失败:', err);
            this.showNotification('复制失败，请手动复制');
          });
        },
      
      viewArticle(id) {
      this.$emit('view-article', id)
    },
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' })
    },
    formatRelativeTime(timestamp) {
      const now = new Date()
      const past = new Date(timestamp)
      const diffMs = now - past
      const diffMins = Math.floor(diffMs / (1000 * 60))
      const diffHours = Math.floor(diffMins / 60)
      const diffDays = Math.floor(diffHours / 24)
      
      if (diffMins < 1) {
        return '刚刚'
      } else if (diffMins < 60) {
        return `${diffMins}分钟前`
      } else if (diffHours < 24) {
        return `${diffHours}小时前`
      } else if (diffDays < 30) {
        return `${diffDays}天前`
      } else {
        return this.formatDate(timestamp)
      }
    },
    getCategoryColor(category) {
      const colorMap = {
        '前端开发': '#4299e1', // blue-500
        '后端开发': '#48bb78', // green-500
        '数据分析': '#ed8936', // yellow-500
        '人工智能': '#9f7aea', // purple-500
        '设计': '#ed64a6', // pink-500
        '移动开发': '#f56565'  // red-500
      }
      
      // 为元素设置CSS变量
      if (this.$el) {
        this.$el.style.setProperty('--category-color', colorMap[category] || '#718096')
      }
      
      return ''
    },
    async submitComment() {
      // 检查用户是否登录
      if (!this.isLoggedIn) {
        this.showNotification('请先登录后再发表评论', 'warning');
        if (this.$parent.switchToAuth) {
          this.$parent.switchToAuth('login');
        }
        return;
      }
      
      if (!this.newComment.trim()) return;
      
      this.isLoading = true;
      
      try {
        // 调用后端API提交评论
        const response = await fetch('http://localhost:5000/api/comments/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            content: this.newComment.trim(),
            article_id: this.article.id,
            author_id: this.currentUser.id,
            parent_id: null
          })
        });
        
        if (!response.ok) {
          throw new Error('提交评论失败');
        }
        
        const data = await response.json();
        
        // 创建评论对象并添加到列表
        const newCommentObj = {
          id: data.id,
          author: this.currentUser.username,
          avatar: this.currentUser.avatar || 'https://picsum.photos/id/1005/100/100',
          content: this.newComment.trim(),
          timestamp: new Date().toISOString(),
          likes: 0,
          replies: []
        };
        
        // 更新文章数据
        if (this.article.comments) {
          this.article.comments.push(newCommentObj)
        } else {
          this.article.comments = [newCommentObj]
        }
        this.article.commentsCount += 1
        
        this.showNotification('评论发表成功！', 'success');
      } catch (error) {
        console.error('提交评论失败:', error);
        // 后备方案
        this.fallbackSubmitComment();
      } finally {
        // 清空评论框
        this.newComment = '';
        this.isLoading = false;
      }
    },
    
    // 评论的后备方案
    fallbackSubmitComment() {
      const newCommentObj = {
        id: Date.now(),
        author: this.currentUser.username,
        avatar: this.currentUser.avatar || 'https://picsum.photos/id/1005/100/100',
        content: this.newComment.trim(),
        timestamp: new Date().toISOString(),
        likes: 0,
        replies: []
      };
      
      // 更新文章数据
      if (this.article.comments) {
        this.article.comments.push(newCommentObj)
      } else {
        this.article.comments = [newCommentObj]
      }
      this.article.commentsCount += 1
      
      this.showNotification('评论已在本地发表（网络异常）', 'warning');
    },
    toggleReplyBox(commentId, targetAuthor = null) {
      this.replyingTo = this.replyingTo === commentId ? null : commentId
      this.replyContent = ''
      this.replyTarget = targetAuthor
    },
    cancelReply() {
      this.replyingTo = null
      this.replyContent = ''
      this.replyTarget = null
    },
    async submitReply(commentId) {
      // 检查用户是否登录
      if (!this.isLoggedIn) {
        this.showNotification('请先登录后再回复评论', 'warning');
        if (this.$parent.switchToAuth) {
          this.$parent.switchToAuth('login');
        }
        return;
      }
      
      if (!this.replyContent.trim()) return;
      
      const comment = this.article.comments.find(c => c.id === commentId);
      if (!comment) return;
      
      this.isLoading = true;
      
      try {
        // 调用后端API提交回复
        const response = await fetch('http://localhost:5000/api/comments/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            content: this.replyContent.trim(),
            article_id: this.article.id,
            author_id: this.currentUser.id,
            parent_id: commentId
          })
        });
        
        if (!response.ok) {
          throw new Error('提交回复失败');
        }
        
        const data = await response.json();
        
        // 创建回复对象并添加到列表
        const replyObj = {
          id: data.id,
          author: this.currentUser.username,
          avatar: this.currentUser.avatar || 'https://picsum.photos/id/1005/100/100',
          content: this.replyContent.trim(),
          timestamp: new Date().toISOString(),
          likes: 0,
          replyTo: comment.author
        };
        
        // 添加回复
        if (comment.replies) {
          comment.replies.push(replyObj);
        } else {
          comment.replies = [replyObj];
        }
        
        this.showNotification('回复发表成功！', 'success');
      } catch (error) {
        console.error('提交回复失败:', error);
        // 后备方案
        this.fallbackSubmitReply(comment);
      } finally {
        // 清空回复框
        this.replyContent = '';
        this.replyingTo = null;
        this.isLoading = false;
      }
    },
    
    // 回复的后备方案
    fallbackSubmitReply(comment) {
      const replyObj = {
        id: Date.now(),
        author: this.currentUser.username,
        avatar: this.currentUser.avatar || 'https://picsum.photos/id/1005/100/100',
        content: this.replyContent.trim(),
        timestamp: new Date().toISOString(),
        likes: 0,
        replyTo: comment.author
      };
      
      if (comment.replies) {
        comment.replies.push(replyObj);
      } else {
        comment.replies = [replyObj];
      }
      
      this.showNotification('回复已在本地发表（网络异常）', 'warning');
    },
    
    // 实现点赞功能
    async toggleLike(comment) {
      // 检查用户是否登录
      if (!this.isLoggedIn) {
        this.showNotification('请先登录后再点赞', 'warning');
        if (this.$parent.switchToAuth) {
          this.$parent.switchToAuth('login');
        }
        return;
      }
      
      // 简单的本地点赞切换（实际项目中应调用API）
      comment.liked = !comment.liked;
      comment.likes = comment.liked ? (comment.likes || 0) + 1 : Math.max(0, (comment.likes || 1) - 1);
      
      // 这里可以添加实际的点赞API调用
    },
    
    // 显示通知
    showNotification(message, type = 'info') {
      // 如果父组件有通知方法，使用父组件的
      if (this.$parent.showNotification) {
        this.$parent.showNotification(message, type);
      } else {
        // 简单的内置通知
        const notification = document.createElement('div');
        notification.className = `fixed bottom-4 right-4 px-6 py-3 rounded-md shadow-lg z-50 transition-all duration-300 transform translate-y-0`;
        
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
        
        setTimeout(() => {
          notification.classList.add('opacity-0', 'translate-y-4');
          setTimeout(() => {
            document.body.removeChild(notification);
          }, 300);
        }, 3000);
      }
    }
  }
}
</script>

<style scoped>
.animate-fadeIn {
  animation: fadeIn 0.3s ease-out forwards;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

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
  background-color: #282c34;
  color: #abb2bf;
  padding: 1rem;
  border-radius: 0.375rem;
  overflow-x: auto;
  margin-bottom: 1rem;
  position: relative;
  font-family: 'Fira Code', 'Courier New', monospace;
}

/* 复制按钮样式 */
.article-content .copy-button {
  position: absolute;
  top: 8px;
  right: 8px;
  background-color: rgba(255, 255, 255, 0.1);
  color: #abb2bf;
  border: none;
  border-radius: 4px;
  padding: 6px 8px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  z-index: 10;
}

.article-content .copy-button:hover {
  background-color: rgba(255, 255, 255, 0.2);
  color: #ffffff;
}



.article-content code {
  font-family: 'Fira Code', monospace;
  font-size: 0.875rem;
  background-color: transparent !important;
  color: inherit;
  padding: 0 !important;
  white-space: pre;
  word-wrap: normal;
}

.comment-actions button, .reply-actions button {
  transition: all 0.2s;
}

.comment-actions button:hover, .reply-actions button:hover {
  transform: translateY(-1px);
}

.not-logged-in-notice {
  background-color: #f0f7ff;
  border-left: 4px solid #4a90e2;
  padding: 12px;
  margin: 15px 0;
  border-radius: 4px;
  color: #333;
}

.not-logged-in-notice button {
  margin-left: 10px;
  background-color: #4a90e2;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.not-logged-in-notice button:hover {
  background-color: #357abd;
}

button {
  cursor: pointer;
  transition: opacity 0.2s, transform 0.2s;
}

button:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

button:active:not(:disabled) {
  transform: scale(0.98);
}
</style>