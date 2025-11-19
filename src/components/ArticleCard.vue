<template>
  <div class="bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow overflow-hidden animate-fadeIn">
    <!-- 文章封面图 -->
    <div v-if="article.coverImage" class="h-48 overflow-hidden">
      <img 
        :src="article.coverImage" 
        :alt="article.title" 
        class="w-full h-full object-cover transition-transform hover:scale-105"
      />
    </div>
    
    <!-- 文章内容 -->
    <div class="p-5">
      <!-- 分类标签 -->
      <div class="flex items-center space-x-2 mb-2">
        <span 
          :class="['inline-block px-2 py-1 text-xs font-medium rounded', getCategoryColor(article.category)]"
          style="background-color: var(--category-color, #4299e1);"
        >
          {{ article.category }}
        </span>
        <span class="text-gray-500 text-sm">{{ formatDate(article.publishedDate) }}</span>
      </div>
      
      <!-- 文章标题 -->
      <h3 class="font-bold text-xl mb-3 line-clamp-2 hover:text-blue-600 transition-colors cursor-pointer" @click="viewArticle(article.id)">
        {{ article.title }}
      </h3>
      
      <!-- 文章摘要 -->
      <p class="text-gray-600 text-sm mb-4 line-clamp-2">
        {{ getArticleExcerpt(article.content) }}
      </p>
      
      <!-- 标签和元信息 -->
      <div class="flex flex-wrap items-center justify-between">
        <!-- 标签 -->
        <div class="flex flex-wrap gap-1 mb-2">
          <span 
            v-for="tag in article.tags" 
            :key="tag"
            class="inline-block px-2 py-0.5 bg-gray-100 text-gray-600 text-xs rounded-full"
          >
            {{ tag }}
          </span>
        </div>
        
        <!-- 统计信息 -->
        <div class="flex items-center space-x-3 text-gray-500 text-sm">
          <span class="flex items-center"><i class="fa fa-eye mr-1"></i> {{ article.views }}</span>
          <span class="flex items-center"><i class="fa fa-heart mr-1"></i> {{ article.likes }}</span>
          <span class="flex items-center"><i class="fa fa-comment mr-1"></i> {{ article.commentsCount }}</span>
        </div>
      </div>
      
      <!-- 作者信息 -->
      <div class="flex items-center mt-4 pt-3 border-t border-gray-100">
        <img :src="article.authorAvatar" :alt="article.author" class="w-8 h-8 rounded-full mr-2" />
        <div>
          <div class="text-sm font-medium text-gray-800">{{ article.author }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ArticleCard',
  props: {
    article: {
      type: Object,
      required: true
    }
  },
  methods: {
    viewArticle(id) {
      this.$emit('view-article', id)
    },
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' })
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
    getArticleExcerpt(content) {
      // 移除HTML标签并获取前100个字符作为摘要
      const plainText = content.replace(/<[^>]*>/g, '').replace(/&nbsp;/g, ' ')
      return plainText.length > 100 ? plainText.substring(0, 100) + '...' : plainText
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