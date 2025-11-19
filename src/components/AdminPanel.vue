<template>
  <div class="bg-white rounded-lg shadow-sm p-6 animate-fadeIn">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold text-gray-800">管理后台</h2>
      <button 
      class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
      @click="$emit('create-article')"
    >
      <i class="fa fa-plus mr-1"></i> 新建文章
    </button>
    </div>
    
    <!-- 统计卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
      <div class="bg-blue-50 p-4 rounded-lg flex items-center justify-between">
        <div>
          <div class="text-sm text-blue-600 font-medium">总文章数</div>
          <div class="text-2xl font-bold text-gray-800">{{ articles.length }}</div>
        </div>
        <div class="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center text-white">
          <i class="fa fa-file-alt text-xl"></i>
        </div>
      </div>
      <div class="bg-green-50 p-4 rounded-lg flex items-center justify-between">
        <div>
          <div class="text-sm text-green-600 font-medium">总分类数</div>
          <div class="text-2xl font-bold text-gray-800">{{ categories.length }}</div>
        </div>
        <div class="w-12 h-12 bg-green-600 rounded-full flex items-center justify-center text-white">
          <i class="fa fa-list text-xl"></i>
        </div>
      </div>
      <div class="bg-purple-50 p-4 rounded-lg flex items-center justify-between">
        <div>
          <div class="text-sm text-purple-600 font-medium">总评论数</div>
          <div class="text-2xl font-bold text-gray-800">{{ totalComments }}</div>
        </div>
        <div class="w-12 h-12 bg-purple-600 rounded-full flex items-center justify-center text-white">
          <i class="fa fa-comment text-xl"></i>
        </div>
      </div>
    </div>
    
    <!-- 管理选项卡 -->
    <div class="border-b border-gray-200 mb-6">
      <nav class="flex -mb-px space-x-8">
        <button 
          class="py-4 px-1 border-b-2 font-medium text-sm" 
          :class="{ 'border-blue-500 text-blue-600': activeTab === 'articles', 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300' : activeTab !== 'articles' }"
          @click="activeTab = 'articles'"
        >
          文章管理
        </button>
        <button 
          class="py-4 px-1 border-b-2 font-medium text-sm" 
          :class="{ 'border-blue-500 text-blue-600': activeTab === 'categories', 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300' : activeTab !== 'categories' }"
          @click="activeTab = 'categories'"
        >
          分类管理
        </button>
        <button 
          class="py-4 px-1 border-b-2 font-medium text-sm" 
          :class="{ 'border-blue-500 text-blue-600': activeTab === 'comments', 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300' : activeTab !== 'comments' }"
          @click="activeTab = 'comments'"
        >
          评论管理
        </button>
      </nav>
    </div>
    
    <!-- 文章管理 -->
    <div v-if="activeTab === 'articles'" class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead>
          <tr>
            <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">标题</th>
            <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">分类</th>
            <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">发布日期</th>
            <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">浏览量</th>
            <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">操作</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="article in articles" :key="article.id">
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="font-medium text-gray-900 line-clamp-1">{{ article.title }}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium" :style="{ backgroundColor: getCategoryColor(article.category) }">
                {{ article.category }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {{ formatDate(article.publishedDate) }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {{ article.views }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
              <button 
          class="text-blue-600 hover:text-blue-900 mr-3"
          @click="$emit('edit-article', article)"
        >
          编辑
        </button>
              <button 
                class="text-red-600 hover:text-red-900"
                @click="deleteArticle(article.id)"
              >
                删除
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <!-- 分类管理 -->
    <div v-else-if="activeTab === 'categories'">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-lg font-medium text-gray-800">分类列表</h3>
        <button 
          class="px-3 py-1 bg-green-600 text-white rounded hover:bg-green-700 transition-colors text-sm"
          @click="showCategoryModal = true"
        >
          <i class="fa fa-plus mr-1"></i> 新建分类
        </button>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div v-for="category in categories" :key="category.id" class="bg-white border border-gray-200 rounded-lg p-4">
          <div class="flex items-center justify-between mb-2">
            <div class="flex items-center">
              <div class="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center mr-2">
                <i :class="['fa', category.icon, 'text-blue-600']"></i>
              </div>
              <div class="font-medium text-gray-800">{{ category.name }}</div>
            </div>
            <div class="flex space-x-2">
              <button 
                class="text-blue-600 hover:text-blue-900 text-sm"
                @click="editCategory(category.id)"
              >
                <i class="fa fa-edit"></i>
              </button>
              <button 
                class="text-red-600 hover:text-red-900 text-sm"
                @click="deleteCategory(category.id)"
              >
                <i class="fa fa-trash"></i>
              </button>
            </div>
          </div>
          <p class="text-gray-600 text-sm mb-2 line-clamp-2">{{ category.description }}</p>
          <div class="text-xs text-gray-500">
            {{ category.count }} 篇文章 · 最后更新于 {{ formatDate(category.lastUpdated) }}
          </div>
        </div>
      </div>
    </div>
    
    <!-- 评论管理 -->
    <div v-else-if="activeTab === 'comments'">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead>
            <tr>
              <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">评论内容</th>
              <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">作者</th>
              <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">文章</th>
              <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">时间</th>
              <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">操作</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="comment in allComments" :key="comment.id">
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 line-clamp-2 max-w-xs">
                {{ comment.content }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <img :src="comment.avatar" :alt="comment.author" class="w-8 h-8 rounded-full mr-2" />
                  <div class="text-sm font-medium text-gray-900">{{ comment.author }}</div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 line-clamp-1">
                {{ getArticleTitleById(comment.articleId) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ formatRelativeTime(comment.timestamp) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <button class="text-red-600 hover:text-red-900">删除</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- 分页 -->
      <div class="flex justify-between items-center mt-4">
        <div class="text-sm text-gray-500">
          显示 1-10 条，共 {{ allComments.length }} 条
        </div>
        <div class="flex space-x-1">
          <button class="px-3 py-1 border rounded text-sm text-gray-600 hover:bg-gray-50 disabled:opacity-50" disabled>
            <i class="fa fa-chevron-left"></i>
          </button>
          <button class="px-3 py-1 border rounded text-sm bg-blue-600 text-white">1</button>
          <button class="px-3 py-1 border rounded text-sm text-gray-600 hover:bg-gray-50">
            <i class="fa fa-chevron-right"></i>
          </button>
        </div>
      </div>
    </div>
    
    <!-- 文章编辑器现在是独立页面，通过事件触发 -->
    
    <!-- 分类编辑模态框 -->
    <category-editor 
      v-if="showCategoryModal"
      :category="currentCategory"
      :available-icons="availableIcons"
      @close="closeCategoryModal"
      @save="saveCategory"
    />
    
    <!-- 删除确认模态框 -->
    <delete-confirm 
      v-if="showDeleteConfirm"
      :message="deleteConfirmMessage"
      @cancel="closeDeleteConfirm"
      @confirm="confirmDelete"
    />
  </div>
</template>

<script>
// import ArticleEditor from './ArticleEditor.vue'
import CategoryEditor from './CategoryEditor.vue'
import DeleteConfirm from './DeleteConfirm.vue'

export default {
  name: 'AdminPanel',
  components: {
    // ArticleEditor,
    CategoryEditor,
    DeleteConfirm
  },
  props: {
    articles: {
      type: Array,
      required: true
    },
    categories: {
      type: Array,
      required: true
    },
    availableIcons: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      activeTab: 'articles',
      showCategoryModal: false,
      showDeleteConfirm: false,
      currentCategory: null,
      deleteItemId: null,
      deleteItemType: null,
      deleteConfirmMessage: ''
    }
  },
  computed: {
    allComments() {
      let comments = []
      if (this.articles && Array.isArray(this.articles)) {
        this.articles.forEach(article => {
          if (article.comments && Array.isArray(article.comments)) {
            article.comments.forEach(comment => {
              comments.push({...comment, articleId: article.id})
              if (comment.replies && Array.isArray(comment.replies)) {
                comment.replies.forEach(reply => {
                  comments.push({...reply, articleId: article.id, isReply: true, parentId: comment.id})
                })
              }
            })
          }
        })
      }
      return comments.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
    },
    totalComments() {
      let count = 0
      this.articles.forEach(article => {
        count += article.commentsCount
      })
      return count
    }
  },
  methods: {
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
      return colorMap[category] || '#718096' // gray-500
    },
    getArticleTitleById(id) {
      const article = this.articles.find(a => a.id === id)
      return article ? article.title : '未知文章'
    },
    // 编辑文章方法现在由父组件处理
    // editArticle(id) {
    //   this.currentArticle = this.articles.find(a => a.id === id)
    //   this.showArticleEditor = true
    // },
    editCategory(id) {
      this.currentCategory = this.categories.find(c => c.id === id)
      this.showCategoryModal = true
    },
    deleteArticle(id) {
      const article = this.articles.find(a => a.id === id)
      if (article) {
        this.deleteItemId = id
        this.deleteItemType = 'article'
        this.deleteConfirmMessage = `确定要删除文章《${article.title}》吗？此操作不可撤销。`
        this.showDeleteConfirm = true
      }
    },
    deleteCategory(id) {
      const category = this.categories.find(c => c.id === id)
      if (category) {
        this.deleteItemId = id
        this.deleteItemType = 'category'
        this.deleteConfirmMessage = `确定要删除分类《${category.name}》吗？该分类下的${category.count}篇文章将受到影响。`
        this.showDeleteConfirm = true
      }
    },
    // 关闭文章编辑器方法现在由父组件处理
    // closeArticleEditor() {
    //   this.showArticleEditor = false
    //   this.currentArticle = null
    // },
    closeCategoryModal() {
      this.showCategoryModal = false
      this.currentCategory = null
    },
    closeDeleteConfirm() {
      this.showDeleteConfirm = false
      this.deleteItemId = null
      this.deleteItemType = null
      this.deleteConfirmMessage = ''
    },
    // 保存文章方法现在通过事件传递原始数据
    saveCategory(categoryData) {
      // 这里应该调用API保存分类，现在只是模拟
      this.$emit('save-category', categoryData)
      this.closeCategoryModal()
    },
    confirmDelete() {
      // 这里应该调用API删除项目，现在只是模拟
      this.$emit('confirm-delete', { type: this.deleteItemType, id: this.deleteItemId })
      this.closeDeleteConfirm()
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
</style>