<template>
  <!-- 主内容区 -->
  <main class="container mx-auto px-4 pt-24 pb-16">
    <!-- 认证视图 -->
    <div v-if="isAuthView">
      <UserLogin v-if="currentAuthView === 'login'" @switchToRegister="$emit('switchToAuth', 'register')" @loginSuccess="$emit('loginSuccess')" />
      <UserRegister v-if="currentAuthView === 'register'" @switchToLogin="$emit('switchToAuth', 'login')" @registerSuccess="$emit('registerSuccess')" />
    </div>
    <!-- 前台视图 -->
    <div v-else-if="!isAdminView">
      <!-- 首页视图 -->
      <div v-if="currentView === 'home'" class="space-y-12">
        <!-- 英雄区 -->
        <section class="relative rounded-2xl overflow-hidden bg-gradient-to-r from-indigo-600 to-purple-700 text-white shadow-xl">
          <div class="absolute inset-0 opacity-20">
            <div class="absolute inset-0 bg-[url('https://picsum.photos/id/1073/1200/400')] bg-cover bg-center"></div>
          </div>
          <div class="relative py-16 px-8 md:py-24 md:px-16 max-w-3xl">
            <h2 class="text-3xl md:text-5xl font-bold mb-4 leading-tight">分享知识，连接思想</h2>
            <p class="text-lg md:text-xl opacity-90 mb-8">探索高质量的文章，参与有意义的讨论，发现新的观点和见解</p>
            <div class="flex flex-wrap gap-4">
              <a href="#" class="bg-white text-indigo-700 hover:bg-gray-100 px-6 py-3 rounded-md font-medium transition-colors" @click.prevent="$emit('switchView', 'articles')">浏览文章</a>
              <a href="#" class="bg-transparent border-2 border-white text-white hover:bg-white/10 px-6 py-3 rounded-md font-medium transition-colors">了解更多</a>
            </div>
          </div>
        </section>
        
        <!-- 特色文章 -->
        <section>
          <div class="flex justify-between items-center mb-8">
            <h2 class="text-2xl font-bold text-gray-800">特色文章</h2>
            <a href="#" class="text-indigo-600 hover:text-indigo-700 font-medium flex items-center" @click.prevent="$emit('switchView', 'articles')">
              查看全部
              <i class="fa fa-arrow-right ml-2"></i>
            </a>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <article v-for="article in featuredArticles" :key="article.id" class="bg-white rounded-xl overflow-hidden shadow-md hover:shadow-xl transition-shadow duration-300 transform hover:-translate-y-1">
              <div class="relative h-48 overflow-hidden">
                <img :src="article.coverImage" alt="Article cover" class="w-full h-full object-cover transition-transform duration-500 hover:scale-110">
                <div class="absolute top-4 left-4">
                  <span :class="`px-3 py-1 rounded-full text-xs font-medium text-white ${getCategoryColor(article.category)}`">
                    {{ article.category }}
                  </span>
                </div>
              </div>
              <div class="p-6">
                <h3 class="text-xl font-bold mb-3 hover:text-indigo-600 transition-colors cursor-pointer">{{ article.title }}</h3>
                <p class="text-gray-600 mb-4 line-clamp-3">{{ article.summary }}</p>
                <div class="flex justify-between items-center">
                  <div class="flex items-center">
                    <img :src="article.authorAvatar" alt="Author" class="w-8 h-8 rounded-full mr-2">
                    <span class="text-sm text-gray-500">{{ article.author }}</span>
                  </div>
                  <span class="text-sm text-gray-500">{{ formatDate(article.publishedDate) }}</span>
                </div>
                <div class="mt-4 pt-4 border-t border-gray-100 flex justify-between items-center">
                  <button class="text-indigo-600 hover:text-indigo-700 font-medium" @click.prevent="$emit('viewArticle', article.id)">阅读全文</button>
                  <div class="flex items-center space-x-4 text-gray-500">
                    <span class="flex items-center"><i class="fa fa-comment-o mr-1"></i> {{ article.commentsCount }}</span>
                    <span class="flex items-center"><i class="fa fa-eye mr-1"></i> {{ article.views }}</span>
                  </div>
                </div>
              </div>
            </article>
          </div>
        </section>
        
        <!-- 分类导航 -->
        <section class="bg-white rounded-xl shadow-md p-8">
          <h2 class="text-2xl font-bold mb-6">文章分类</h2>
          <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
            <a v-for="category in categories" :key="category.id" href="#" class="flex flex-col items-center p-6 rounded-lg border border-gray-100 hover:border-indigo-200 hover:bg-indigo-50 transition-colors group" @click.prevent="$emit('filterArticlesByCategory', category.name)">
              <div class="w-12 h-12 rounded-full flex items-center justify-center mb-3 bg-indigo-100 text-indigo-600 group-hover:bg-indigo-600 group-hover:text-white transition-colors">
                <i :class="category.icon + ' text-xl'"></i>
              </div>
              <h3 class="font-medium text-center">{{ category.name }}</h3>
              <span class="text-sm text-gray-500 mt-1">{{ category.count }} 篇文章</span>
            </a>
          </div>
        </section>
        
        <!-- 最新文章 -->
        <section>
          <h2 class="text-2xl font-bold mb-8">最新文章</h2>
          <div class="space-y-6">
            <div v-for="article in latestArticles" :key="article.id" class="bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow p-6 flex flex-col md:flex-row gap-6">
              <div class="md:w-1/4 lg:w-1/5 relative rounded-lg overflow-hidden">
                <img :src="article.coverImage" alt="Article cover" class="w-full h-48 object-cover">
                <span :class="`absolute top-3 left-3 px-3 py-1 rounded-full text-xs font-medium text-white ${getCategoryColor(article.category)}`">
                  {{ article.category }}
                </span>
              </div>
              <div class="md:w-3/4 lg:w-4/5 flex flex-col">
                <h3 class="text-xl font-bold mb-2 hover:text-indigo-600 transition-colors cursor-pointer">{{ article.title }}</h3>
                <p class="text-gray-600 mb-4 flex-grow line-clamp-2">{{ article.summary }}</p>
                <div class="flex flex-wrap justify-between items-center gap-4">
                  <div class="flex items-center">
                    <img :src="article.authorAvatar" alt="Author" class="w-8 h-8 rounded-full mr-2">
                    <span class="text-sm text-gray-500">{{ article.author }} · {{ formatDate(article.publishedDate) }}</span>
                  </div>
                  <div class="flex items-center space-x-4 text-gray-500">
                    <span class="flex items-center"><i class="fa fa-comment-o mr-1"></i> {{ article.commentsCount }}</span>
                    <span class="flex items-center"><i class="fa fa-eye mr-1"></i> {{ article.views }}</span>
                    <button class="text-indigo-600 hover:text-indigo-700 font-medium" @click.prevent="$emit('viewArticle', article.id)">阅读全文</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="mt-8 text-center">
            <button class="bg-white border border-gray-300 hover:bg-gray-50 text-gray-700 px-6 py-3 rounded-md font-medium transition-colors">
              加载更多
              <i class="fa fa-refresh ml-2"></i>
            </button>
          </div>
        </section>
      </div>
      
      <!-- 文章列表视图 -->
      <div v-if="currentView === 'articles'" class="space-y-8">
        <div class="bg-white rounded-xl shadow-md p-6">
          <h2 class="text-2xl font-bold mb-6">所有文章</h2>
          
          <!-- 筛选和排序 -->
          <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 gap-4">
            <div class="flex flex-wrap gap-2">
              <button class="px-4 py-2 rounded-full text-sm bg-indigo-100 text-indigo-700 hover:bg-indigo-200 transition-colors" @click="$emit('clearCategoryFilter')">全部</button>
              <button v-for="category in categories" :key="category.id" class="px-4 py-2 rounded-full text-sm" :class="filteredCategory === category.name ? 'bg-indigo-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'" @click="$emit('filterArticlesByCategory', category.name)">
                {{ category.name }}
              </button>
            </div>
            
            <div class="relative">
              <select class="appearance-none bg-gray-100 border-0 pl-4 pr-10 py-2 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500">
                <option>最新发布</option>
                <option>最多阅读</option>
                <option>最多评论</option>
              </select>
              <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
                <i class="fa fa-chevron-down text-xs"></i>
              </div>
            </div>
          </div>
          
          <!-- 文章网格 -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <article v-for="article in filteredArticles" :key="article.id" class="bg-white rounded-xl overflow-hidden shadow-sm hover:shadow-md transition-shadow border border-gray-100">
              <div class="relative h-48 overflow-hidden">
                <img :src="article.coverImage" alt="Article cover" class="w-full h-full object-cover transition-transform duration-500 hover:scale-110">
                <div class="absolute top-4 left-4">
                  <span :class="`px-3 py-1 rounded-full text-xs font-medium text-white ${getCategoryColor(article.category)}`">
                    {{ article.category }}
                  </span>
                </div>
              </div>
              <div class="p-5">
                <h3 class="text-lg font-bold mb-2 hover:text-indigo-600 transition-colors cursor-pointer">{{ article.title }}</h3>
                <p class="text-gray-600 text-sm mb-3 line-clamp-2">{{ article.summary }}</p>
                <div class="flex justify-between items-center text-sm text-gray-500">
                  <span>{{ formatDate(article.publishedDate) }}</span>
                  <span class="flex items-center"><i class="fa fa-comment-o mr-1"></i> {{ article.commentsCount }}</span>
                </div>
                <button class="mt-3 w-full text-center text-indigo-600 hover:text-indigo-700 text-sm font-medium" @click.prevent="$emit('viewArticle', article.id)">阅读全文</button>
              </div>
            </article>
          </div>
          
          <!-- 分页 -->
          <div class="mt-8 flex justify-center">
            <nav class="inline-flex rounded-md shadow-sm">
              <button class="px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 rounded-l-md">
                <i class="fa fa-chevron-left"></i>
              </button>
              <button class="px-4 py-2 border-t border-b border-gray-300 bg-indigo-50 text-sm font-medium text-indigo-600">1</button>
              <button class="px-4 py-2 border-t border-b border-gray-300 bg-white text-sm font-medium text-gray-700 hover:bg-gray-50">2</button>
              <button class="px-4 py-2 border-t border-b border-gray-300 bg-white text-sm font-medium text-gray-700 hover:bg-gray-50">3</button>
              <button class="px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 rounded-r-md">
                <i class="fa fa-chevron-right"></i>
              </button>
            </nav>
          </div>
        </div>
      </div>
      
      <!-- 分类视图 -->
      <div v-if="currentView === 'categories'" class="space-y-8">
        <div class="bg-white rounded-xl shadow-md p-6">
          <h2 class="text-2xl font-bold mb-6">文章分类</h2>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div v-for="category in categories" :key="category.id" class="flex items-start p-5 rounded-lg border border-gray-100 hover:border-indigo-200 hover:bg-indigo-50 transition-colors group cursor-pointer" @click="$emit('filterArticlesByCategory', category.name)">
              <div class="w-12 h-12 rounded-full flex items-center justify-center mr-4 bg-indigo-100 text-indigo-600 group-hover:bg-indigo-600 group-hover:text-white transition-colors flex-shrink-0">
                <i :class="category.icon + ' text-xl'"></i>
              </div>
              <div class="flex-grow">
                <h3 class="font-bold text-lg mb-1">{{ category.name }}</h3>
                <p class="text-gray-600 text-sm mb-2">{{ category.description }}</p>
                <div class="flex items-center text-sm text-gray-500">
                  <span>{{ category.count }} 篇文章</span>
                  <span class="mx-2">•</span>
                  <span>最后更新: {{ category.lastUpdated }}</span>
                </div>
              </div>
              <div class="flex-shrink-0 ml-2 text-indigo-600 opacity-0 group-hover:opacity-100 transition-opacity">
                <i class="fa fa-arrow-right"></i>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 文章详情视图 -->
      <div v-if="currentView === 'articleDetail'" class="space-y-8">
        <article class="bg-white rounded-xl shadow-md overflow-hidden">
          <div class="relative h-64 md:h-80 lg:h-96">
            <img :src="currentArticle?.coverImage" alt="Article cover" class="w-full h-full object-cover">
            <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
            <div class="absolute bottom-0 left-0 right-0 p-6 md:p-8 text-white">
              <span :class="`px-3 py-1 rounded-full text-xs font-medium mb-4 inline-block ${getCategoryColor(currentArticle?.category)}`">
                {{ currentArticle?.category }}
              </span>
              <h1 class="text-2xl md:text-3xl lg:text-4xl font-bold mb-3">{{ currentArticle?.title }}</h1>
              <div class="flex flex-wrap items-center gap-4 text-sm text-white/90">
                <div class="flex items-center">
                  <img :src="currentArticle?.authorAvatar" alt="Author" class="w-6 h-6 rounded-full mr-2">
                  <span>{{ currentArticle?.author }}</span>
                </div>
                <span>{{ currentArticle?.publishedDate && formatDate(currentArticle.publishedDate) }}</span>
                <span class="flex items-center"><i class="fa fa-eye mr-1"></i> {{ currentArticle?.views }}</span>
              </div>
            </div>
          </div>
          
          <div class="p-6 md:p-8 lg:p-10">
            <div class="prose max-w-none">
              <div v-html="currentArticle?.content" class="article-content space-y-6"></div>
            </div>
            
            <!-- 标签 -->
            <div class="mt-8 pt-6 border-t border-gray-100">
              <div class="flex flex-wrap items-center gap-2">
                <span class="text-gray-500">标签:</span>
                <span v-for="tag in currentArticle?.tags" :key="tag" class="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm">#{{ tag }}</span>
              </div>
            </div>
            
            <!-- 分享 -->
            <div class="mt-6 flex items-center justify-between">
              <div class="flex items-center gap-3">
                <button class="flex items-center gap-1 px-3 py-2 bg-gray-100 hover:bg-gray-200 rounded-md text-sm transition-colors">
                  <i class="fa fa-heart-o text-red-500"></i>
                  <span>喜欢 ({{ currentArticle?.likes }})</span>
                </button>
                <button class="flex items-center gap-1 px-3 py-2 bg-gray-100 hover:bg-gray-200 rounded-md text-sm transition-colors">
                  <i class="fa fa-bookmark-o"></i>
                  <span>收藏</span>
                </button>
              </div>
              
              <div class="flex items-center gap-2">
                <span class="text-sm text-gray-500">分享:</span>
                <button class="w-8 h-8 rounded-full bg-[#1877F2] flex items-center justify-center text-white hover:bg-[#166FE5] transition-colors">
                  <i class="fa fa-facebook"></i>
                </button>
                <button class="w-8 h-8 rounded-full bg-[#1DA1F2] flex items-center justify-center text-white hover:bg-[#1a91da] transition-colors">
                  <i class="fa fa-twitter"></i>
                </button>
                <button class="w-8 h-8 rounded-full bg-[#25D366] flex items-center justify-center text-white hover:bg-[#22c15c] transition-colors">
                  <i class="fa fa-whatsapp"></i>
                </button>
                <button class="w-8 h-8 rounded-full bg-[#0A66C2] flex items-center justify-center text-white hover:bg-[#095cb5] transition-colors">
                  <i class="fa fa-linkedin"></i>
                </button>
              </div>
            </div>
          </div>
        </article>
        
        <!-- 作者信息 -->
        <div class="bg-white rounded-xl shadow-md p-6 flex flex-col md:flex-row items-center gap-6">
          <img :src="currentArticle?.authorAvatar" alt="Author" class="w-20 h-20 rounded-full object-cover border-4 border-white shadow-md">
          <div class="text-center md:text-left">
            <h3 class="text-xl font-bold mb-1">{{ currentArticle?.author }}</h3>
            <p class="text-gray-600 mb-3">{{ currentArticle?.authorBio }}</p>
            <button class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md text-sm transition-colors">
              关注作者
            </button>
          </div>
        </div>
        
        <!-- 评论区 -->
        <div class="bg-white rounded-xl shadow-md p-6">
          <h3 class="text-xl font-bold mb-6">评论 ({{ currentArticle?.commentsCount }})</h3>
          
          <!-- 评论输入 -->
          <div class="mb-8">
            <div class="flex gap-4">
              <img :src="currentUser ? currentUser.avatar : 'https://picsum.photos/id/64/100/100'" alt="Your avatar" class="w-10 h-10 rounded-full">
              <div class="flex-grow">
                <textarea v-model="commentContent" :placeholder="currentUser ? '分享你的想法...' : '请登录后发表评论...'" class="w-full border border-gray-300 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 resize-none" rows="3" :disabled="!currentUser || isSubmittingComment"></textarea>
                <div class="mt-3 flex justify-between items-center">
                  <div class="flex gap-2">
                    <button class="w-8 h-8 rounded-full bg-gray-100 hover:bg-gray-200 flex items-center justify-center text-gray-700 transition-colors" disabled>
                      <i class="fa fa-image"></i>
                    </button>
                    <button class="w-8 h-8 rounded-full bg-gray-100 hover:bg-gray-200 flex items-center justify-center text-gray-700 transition-colors" disabled>
                      <i class="fa fa-smile-o"></i>
                    </button>
                  </div>
                  <div>
                    <button v-if="!currentUser" class="bg-gray-200 text-gray-600 px-4 py-2 rounded-md text-sm transition-colors mr-2" @click="$emit('showAuthView', 'login')">
                      登录
                    </button>
                    <button :class="['px-4 py-2 rounded-md text-sm transition-colors', currentUser && !isSubmittingComment ? 'bg-indigo-600 hover:bg-indigo-700 text-white' : 'bg-gray-200 text-gray-600 cursor-not-allowed']" @click="submitComment" :disabled="!currentUser || isSubmittingComment || !commentContent.trim()">
                      {{ isSubmittingComment ? '发表中...' : '发表评论' }}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 评论列表 -->
          <div class="space-y-6">
            <div v-for="comment in currentArticle?.comments" :key="comment.id" class="border-b border-gray-100 pb-6 last:border-0 last:pb-0">
              <div class="flex gap-4">
                <img :src="comment.authorAvatar" alt="Comment author" class="w-10 h-10 rounded-full">
                <div class="flex-grow">
                  <div class="bg-gray-50 p-4 rounded-lg">
                    <div class="flex justify-between items-start mb-2">
                      <h4 class="font-medium">{{ comment.author }}</h4>
                      <span class="text-xs text-gray-500">{{ formatRelativeTime(comment.timestamp) }}</span>
                    </div>
                    <p class="text-gray-700">{{ comment.content }}</p>
                  </div>
                  <div class="mt-2 flex items-center gap-4 text-sm">
                    <button class="text-gray-500 hover:text-indigo-600 transition-colors flex items-center gap-1" @click="toggleLike(comment)">
                      <i :class="comment.isLiked ? 'fa fa-heart text-red-500' : 'fa fa-heart-o'"></i>
                      <span>{{ comment.likes }}</span>
                    </button>
                    <button class="text-gray-500 hover:text-indigo-600 transition-colors" @click="toggleReplyBox(comment)">回复</button>
                  </div>
                  
                  <!-- 嵌套回复 -->
                  <div class="mt-4 ml-6 space-y-4">
                    <div v-for="reply in comment.replies" :key="reply.id" class="flex gap-3">
                      <img :src="reply.authorAvatar" alt="Reply author" class="w-8 h-8 rounded-full">
                      <div class="flex-grow">
                        <div class="bg-gray-50 p-3 rounded-lg text-sm">
                          <div class="flex justify-between items-start mb-1">
                            <h5 class="font-medium">{{ reply.author }}</h5>
                            <span class="text-xs text-gray-500">{{ formatRelativeTime(reply.timestamp) }}</span>
                          </div>
                          <p class="text-gray-700">{{ reply.content }}</p>
                        </div>
                        <div class="mt-1 flex items-center gap-4 text-xs">
                          <button class="text-gray-500 hover:text-indigo-600 transition-colors flex items-center gap-1" @click="toggleLike(reply, comment)">
                            <i :class="reply.isLiked ? 'fa fa-heart text-red-500' : 'fa fa-heart-o'"></i>
                            <span>{{ reply.likes }}</span>
                          </button>
                          <button class="text-gray-500 hover:text-indigo-600 transition-colors" @click="toggleReplyBox(comment, reply)">回复</button>
                        </div>
                      </div>
                    </div>
                      
                    <!-- 回复输入框 -->
                    <div v-if="replyBoxVisible.commentId === comment.id" class="flex gap-3">
                      <img :src="currentUser ? currentUser.avatar : 'https://picsum.photos/id/64/100/100'" alt="Your avatar" class="w-8 h-8 rounded-full">
                      <div class="flex-grow">
                        <textarea v-model="replyBoxVisible.content" :placeholder="replyBoxVisible.replyTo ? `回复 @${replyBoxVisible.replyTo.author}...` : `回复 @${comment.author}...`" class="w-full border border-gray-300 rounded-lg p-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 resize-none" rows="2" :disabled="!currentUser || isSubmittingReply"></textarea>
                        <div class="mt-2 flex justify-end gap-2">
                          <button class="px-3 py-1 border border-gray-300 text-gray-700 rounded-md text-sm hover:bg-gray-50 transition-colors" @click="cancelReply">取消</button>
                          <button :class="['px-3 py-1 rounded-md text-sm transition-colors', currentUser && !isSubmittingReply ? 'bg-indigo-600 text-white hover:bg-indigo-700' : 'bg-gray-200 text-gray-600 cursor-not-allowed']" @click="submitReply(comment)" :disabled="!currentUser || isSubmittingReply || !replyBoxVisible.content.trim()">
                            {{ isSubmittingReply ? '回复中...' : '回复' }}
                          </button>
                        </div>
                      </div>
                    </div>
                      
                    <!-- 显示回复按钮 -->
                    <button v-else class="flex items-center text-sm text-indigo-600 hover:text-indigo-700" @click="toggleReplyBox(comment)">
                      <i class="fa fa-reply mr-1"></i>
                      <span>回复 @{{ comment.author }}</span>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 加载更多评论 -->
          <div class="mt-6 text-center">
            <button class="bg-white border border-gray-300 hover:bg-gray-50 text-gray-700 px-4 py-2 rounded-md text-sm font-medium transition-colors">
              查看更多评论
            </button>
          </div>
        </div>
        
        <!-- 相关文章 -->
        <div>
          <h3 class="text-xl font-bold mb-6">相关推荐</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <article v-for="article in relatedArticles" :key="article.id" class="bg-white rounded-xl overflow-hidden shadow-sm hover:shadow-md transition-shadow border border-gray-100">
              <div class="relative h-40 overflow-hidden">
                <img :src="article.coverImage" alt="Article cover" class="w-full h-full object-cover transition-transform duration-500 hover:scale-110">
              </div>
              <div class="p-4">
                <h3 class="text-base font-bold mb-2 hover:text-indigo-600 transition-colors cursor-pointer line-clamp-2">{{ article.title }}</h3>
                <div class="flex justify-between items-center text-xs text-gray-500">
                  <span>{{ formatDate(article.publishedDate) }}</span>
                  <span class="flex items-center"><i class="fa fa-comment-o mr-1"></i> {{ article.commentsCount }}</span>
                </div>
              </div>
            </article>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 管理后台视图 - 使用内部状态控制 -->
    <div v-if="internalShowAdminView && !showArticleEditor" class="space-y-8">
        <AdminPanel 
            :articles="articles" 
            :categories="categories" 
            :available-icons="availableIcons"
            @save-article="handleSaveArticle"
            @save-category="handleSaveCategory"
            @confirm-delete="handleConfirmDelete"
            @create-article="createArticle"
            @edit-article="editArticle"
          />
      </div>
      
      <!-- 独立的文章编辑器页面 -->
      <div v-if="showArticleEditor" class="min-h-screen">
        <article-editor
          :article="editingArticle"
          :categories="categories"
          @save="handleSaveArticle"
          @cancel="cancelEditArticle"
        />
      </div>
  </main>
</template>

<script>
import UserLogin from './UserLogin.vue'
import UserRegister from './UserRegister.vue'
import AdminPanel from './AdminPanel.vue'
import ArticleEditor from './ArticleEditor.vue'

export default {
  name: 'BlogMain',
  components: {
    UserLogin,
    UserRegister,
    AdminPanel,
    ArticleEditor
  },
  props: {
    // 视图状态
    isAdminView: {
      type: Boolean,
      default: false
    },
    currentView: {
      type: String,
      default: 'home'
    },
    adminTab: {
      type: String,
      default: 'articles'
    },
    // 认证相关状态
    isAuthView: {
      type: Boolean,
      default: false
    },
    currentAuthView: {
      type: String,
      default: 'login'
    },
    currentUser: {
      type: Object,
      default: null
    },
    // 数据
    articles: {
      type: Array,
      default: () => []
    },
    categories: {
      type: Array,
      default: () => []
    },
    currentArticle: {
      type: Object,
      default: null
    },
    relatedArticles: {
      type: Array,
      default: () => []
    },
    filteredCategory: {
      type: String,
      default: null
    }
  },
  data() {
    return {
      // 评论相关状态
      commentContent: '',
      isSubmittingComment: false,
      isSubmittingReply: false,
      replyBoxVisible: { commentId: null, replyTo: null, content: '' },
      // 编辑文章相关状态
      showArticleEditor: false,
      editingArticle: null,
      // 内部管理视图状态
      internalShowAdminView: false,
      // 可用的图标列表
      availableIcons: [
        'fa-laptop',
        'fa-server',
        'fa-database',
        'fa-robot',
        'fa-paint-brush',
        'fa-mobile-alt',
        'fa-globe',
        'fa-code',
        'fa-file-alt',
        'fa-chart-bar'
      ]
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
    
    // 总评论数
    totalComments() {
      let count = 0;
      this.articles.forEach(article => {
        count += article.commentsCount || 0;
      });
      return count;
    },
    
    // 总访问量
    totalViews() {
      let count = 0;
      this.articles.forEach(article => {
        count += article.views || 0;
      });
      return count;
    }
  },
  watch: {
    // 监听外部isAdminView的变化，同步到内部状态
    isAdminView(newVal) {
      // 只有在非编辑状态下才同步外部状态
      if (!this.showArticleEditor) {
        this.internalShowAdminView = newVal
      }
    }
  },
  
  mounted() {
    // 组件挂载时初始化内部状态
    this.internalShowAdminView = this.isAdminView
  },
  
  methods: {
    // 简化的文章保存处理方法
    handleSaveArticle(articleData) {
      console.log('handleSaveArticle接收到数据:', articleData)
      
      // 为新文章生成临时ID
      const articleId = articleData.id || Date.now()
      
      // 查找分类信息
      const category = this.categories.find(c => c.id === articleData.category_id)
      
      // 构建完整文章数据
      const completeArticleData = {
        ...articleData,
        id: articleId,
        category: category ? category.name : '',
        commentsCount: 0,
        views: 0
      }
      
      // 如果是编辑现有文章，保留原有统计信息
      if (articleData.id) {
        const existingArticle = this.articles.find(a => a.id === articleData.id)
        if (existingArticle) {
          completeArticleData.commentsCount = existingArticle.commentsCount || 0
          completeArticleData.views = existingArticle.views || 0
        }
      }
      
      console.log('发送saveArticle事件:', completeArticleData)
      
      // 发送事件给父组件
      this.$emit('saveArticle', completeArticleData)
      
      // 立即更新UI状态
      this.showArticleEditor = false
      this.editingArticle = null
      this.internalShowAdminView = true
      
      console.log('UI状态已更新')
    },
    
    // 处理分类保存事件
    handleSaveCategory(categoryData) {
      // 这里应该调用API保存分类，现在只是模拟
      this.$emit('saveCategory', categoryData)
    },
    
    // 处理删除确认事件
    handleConfirmDelete({ type, id }) {
      // 这里应该调用API删除项目，现在只是模拟
      this.$emit('deleteItem', { type, id })
    },
    
    // 创建新文章
    createArticle() {
      this.showArticleEditor = true
      this.editingArticle = null
      this.internalShowAdminView = false // 使用内部状态控制
    },
    
    // 编辑文章
    editArticle(article) {
      this.showArticleEditor = true
      this.editingArticle = article
      this.internalShowAdminView = false // 使用内部状态控制
    },
    
    // 取消编辑文章
    cancelEditArticle() {
      this.showArticleEditor = false
      this.editingArticle = null
      this.internalShowAdminView = true // 使用内部状态控制
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
        
        // 更新本地数据并通过事件通知父组件
        this.$emit('commentSubmitted', newComment);
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
        
        // 更新本地数据并通过事件通知父组件
        this.$emit('replySubmitted', { comment, reply: newReply });
        
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
    async toggleLike(item, parentComment = null) {
      try {
        // 切换本地点赞状态
        item.isLiked = !item.isLiked;
        item.likes += item.isLiked ? 1 : -1;
        
        // 通知父组件更新
        this.$emit('likeToggled', { item, parentComment });
        
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
    
    // 显示通知
    showNotification(message, type = 'success') {
      const notification = document.createElement('div');
      notification.className = 'fixed top-4 right-4 py-3 px-5 rounded-md shadow-lg transform transition-all duration-300 z-50';
      
      if (type === 'success') {
        notification.classList.add('bg-green-500', 'text-white');
      } else if (type === 'error') {
        notification.classList.add('bg-red-500', 'text-white');
      } else if (type === 'info') {
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
    }
  }
}
</script>

<style scoped>
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