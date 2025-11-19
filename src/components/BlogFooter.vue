<template>
  <footer class="bg-gray-800 text-white py-12">
    <div class="container mx-auto px-4">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
        <!-- 网站信息 -->
        <div>
          <div class="flex items-center space-x-2 mb-4">
            <i class="fa fa-feather-alt text-blue-400 text-2xl"></i>
            <span class="font-bold text-xl">智慧博客</span>
          </div>
          <p class="text-gray-400 mb-4">分享知识，连接思想，探索无限可能。</p>
          <div class="flex space-x-4">
            <a href="#" class="text-gray-400 hover:text-white transition-colors"><i class="fa fa-twitter"></i></a>
            <a href="#" class="text-gray-400 hover:text-white transition-colors"><i class="fa fa-facebook"></i></a>
            <a href="#" class="text-gray-400 hover:text-white transition-colors"><i class="fa fa-instagram"></i></a>
            <a href="#" class="text-gray-400 hover:text-white transition-colors"><i class="fa fa-github"></i></a>
          </div>
        </div>
        
        <!-- 快速链接 -->
        <div>
          <h3 class="font-medium text-lg mb-4">快速链接</h3>
          <ul class="space-y-2">
            <li><a href="#" class="text-gray-400 hover:text-white transition-colors">关于我们</a></li>
            <li><a href="#" class="text-gray-400 hover:text-white transition-colors">联系方式</a></li>
            <li><a href="#" class="text-gray-400 hover:text-white transition-colors">隐私政策</a></li>
            <li><a href="#" class="text-gray-400 hover:text-white transition-colors">使用条款</a></li>
            <li><a href="#" class="text-gray-400 hover:text-white transition-colors">投稿指南</a></li>
          </ul>
        </div>
        
        <!-- 热门分类 -->
        <div>
          <h3 class="font-medium text-lg mb-4">热门分类</h3>
          <ul class="space-y-2">
            <li v-for="category in popularCategories" :key="category.id">
              <a href="#" class="text-gray-400 hover:text-white transition-colors flex items-center justify-between">
                <span>{{ category.name }}</span>
              </a>
            </li>
          </ul>
        </div>
        
        <!-- 订阅 -->
        <div>
          <h3 class="font-medium text-lg mb-4">订阅更新</h3>
          <p class="text-gray-400 mb-4">订阅我们的通讯，获取最新文章和资讯。</p>
          <form class="space-y-2">
            <input 
              type="email" 
              placeholder="您的邮箱地址" 
              class="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button 
              type="submit" 
              class="w-full px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              订阅
            </button>
          </form>
        </div>
      </div>
      
      <div class="border-t border-gray-700 mt-8 pt-8 text-center text-gray-400 text-sm">
        <p>© 2023 智慧博客. 保留所有权利。</p>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'BlogFooter',
  props: {
    categories: {
      type: Array,
      required: true
    }
  },
  computed: {
    popularCategories() {
      // 确保categories是数组才进行处理
      if (!Array.isArray(this.categories)) {
        return []
      }
      // 获取文章数量最多的5个分类
      return [...this.categories]
        .sort((a, b) => (b.count || 0) - (a.count || 0))
        .slice(0, 5)
    }
  }
}
</script>

<style scoped>
/* 页脚样式已集成在组件中 */
</style>