<template>
  <!-- 导航栏 -->
  <header>
    <nav class="bg-white shadow-md fixed w-full z-50 transition-all duration-300" :class="{ 'bg-white/90 backdrop-blur-sm shadow-lg': isScrolled }">
      <div class="container mx-auto px-4 py-3 flex justify-between items-center">
        <div class="flex items-center space-x-2">
          <i class="fa fa-book text-indigo-600 text-2xl"></i>
          <h1 class="text-xl font-bold text-indigo-700">InsightBlog</h1>
        </div>
        
        <!-- 桌面导航 -->
        <div class="hidden md:flex items-center space-x-8">
          <a href="#" class="text-gray-700 hover:text-indigo-600 transition-colors font-medium" @click.prevent="switchView('home')">首页</a>
          <a href="#" class="text-gray-700 hover:text-indigo-600 transition-colors font-medium" @click.prevent="switchView('articles')">文章</a>
          <a href="#" class="text-gray-700 hover:text-indigo-600 transition-colors font-medium" @click.prevent="switchView('categories')">分类</a>
          <div v-if="!isAdminView" class="relative group">
            <button class="flex items-center text-gray-700 hover:text-indigo-600 transition-colors font-medium">
              搜索
              <i class="fa fa-search ml-1"></i>
            </button>
            <div class="absolute right-0 mt-2 w-64 bg-white rounded-md shadow-lg py-1 z-10 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 transform group-hover:translate-y-0 translate-y-2">
              <div class="p-2">
                <input type="text" placeholder="搜索文章..." class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500">
              </div>
            </div>
          </div>
          <!-- 用户认证相关导航 -->
          <div v-if="!currentUser" class="flex items-center space-x-4">
            <a href="#" class="text-gray-700 hover:text-indigo-600 transition-colors font-medium" @click.prevent="switchToAuth('login')">登录</a>
            <a href="#" class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md transition-colors font-medium" @click.prevent="switchToAuth('register')">注册</a>
          </div>
          <div v-else class="relative group">
            <button class="flex items-center text-gray-700 hover:text-indigo-600 transition-colors font-medium">
              <img :src="currentUser.avatar || 'https://picsum.photos/id/64/40/40'" alt="用户头像" class="w-8 h-8 rounded-full mr-2 object-cover">
              <span>{{ currentUser.username }}</span>
              <i class="fa fa-chevron-down ml-1 text-xs"></i>
            </button>
            <div class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-10 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 transform group-hover:translate-y-0 translate-y-2">
              <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100" @click.prevent="showUserProfile">个人资料</a>
              <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100" @click.prevent="toggleAdminView" v-if="currentUser.isAdmin">管理后台</a>
              <div class="border-t border-gray-100 my-1"></div>
              <a href="#" class="block px-4 py-2 text-sm text-red-600 hover:bg-gray-100" @click.prevent="handleLogout">退出登录</a>
            </div>
          </div>
          <button v-if="!currentUser && !isAuthView" @click="toggleAdminView" class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md transition-colors flex items-center">
            <i class="fa fa-cog mr-2"></i>
            <span>{{ isAdminView ? '返回前台' : '管理后台' }}</span>
          </button>
        </div>
        
        <!-- 移动端菜单按钮 -->
        <button class="md:hidden text-gray-700" @click="mobileMenuOpen = !mobileMenuOpen">
          <i class="fa fa-bars text-xl"></i>
        </button>
      </div>
      
      <!-- 移动端导航菜单 -->
      <div class="md:hidden bg-white border-t" v-if="mobileMenuOpen">
        <div class="container mx-auto px-4 py-2 flex flex-col space-y-3">
          <a href="#" class="py-2 text-gray-700 hover:text-indigo-600 transition-colors font-medium" @click.prevent="switchView('home'); mobileMenuOpen = false">首页</a>
          <a href="#" class="py-2 text-gray-700 hover:text-indigo-600 transition-colors font-medium" @click.prevent="switchView('articles'); mobileMenuOpen = false">文章</a>
          <a href="#" class="py-2 text-gray-700 hover:text-indigo-600 transition-colors font-medium" @click.prevent="switchView('categories'); mobileMenuOpen = false">分类</a>
          <div class="py-2">
            <input type="text" placeholder="搜索文章..." class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500">
          </div>
          <!-- 移动端认证相关导航 -->
          <div v-if="!currentUser">
            <a href="#" class="py-2 text-gray-700 hover:text-indigo-600 transition-colors font-medium" @click.prevent="switchToAuth('login'); mobileMenuOpen = false">登录</a>
            <a href="#" class="py-2 bg-indigo-600 hover:bg-indigo-700 text-white px-4 rounded-md transition-colors font-medium block text-center" @click.prevent="switchToAuth('register'); mobileMenuOpen = false">注册</a>
          </div>
          <div v-else>
            <div class="flex items-center py-2 px-3 bg-gray-50 rounded-md">
              <img :src="currentUser.avatar || 'https://picsum.photos/id/64/40/40'" alt="用户头像" class="w-10 h-10 rounded-full mr-3 object-cover">
              <div>
                <div class="font-medium text-gray-900">{{ currentUser.username }}</div>
                <div class="text-xs text-gray-500">{{ currentUser.email }}</div>
              </div>
            </div>
            <a href="#" class="py-2 text-gray-700 hover:text-indigo-600 transition-colors font-medium" @click.prevent="showUserProfile; mobileMenuOpen = false">个人资料</a>
            <a href="#" class="py-2 text-gray-700 hover:text-indigo-600 transition-colors font-medium" @click.prevent="toggleAdminView; mobileMenuOpen = false" v-if="currentUser.isAdmin">管理后台</a>
            <a href="#" class="py-2 text-red-600 hover:text-red-700 transition-colors font-medium" @click.prevent="handleLogout; mobileMenuOpen = false">退出登录</a>
          </div>
          <button v-if="!currentUser && !isAuthView" @click="toggleAdminView; mobileMenuOpen = false" class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md transition-colors flex items-center justify-center mt-2">
            <i class="fa fa-cog mr-2"></i>
            <span>{{ isAdminView ? '返回前台' : '管理后台' }}</span>
          </button>
        </div>
      </div>
    </nav>
  </header>
</template>

<script>
export default {
  name: 'BlogHeader',
  props: {
    currentView: {
      type: String,
      required: true
    },
    isAdminView: {
      type: Boolean,
      required: true
    },
    isScrolled: {
      type: Boolean,
      required: true
    },
    currentUser: {
      type: Object,
      default: null
    },
    isAuthView: {
      type: Boolean,
      required: true
    }
  },
  data() {
    return {
      mobileMenuOpen: false
    }
  },
  methods: {
    switchView(view) {
      this.$emit('switch-view', view)
    },
    switchToAuth(authType) {
      this.$emit('switch-to-auth', authType)
    },
    toggleAdminView() {
      this.$emit('toggle-admin-view')
    },
    showUserProfile() {
      this.$emit('show-user-profile')
    },
    handleLogout() {
      this.$emit('handle-logout')
    }
  }
}
</script>

<style scoped>
/* 导航栏样式已集成在组件中 */
</style>