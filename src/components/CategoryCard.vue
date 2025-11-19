<template>
  <div class="bg-white rounded-lg shadow-sm hover:shadow-md transition-all p-4 cursor-pointer animate-fadeIn" @click="filterByCategory(category.name)">
    <div class="flex items-center justify-between">
      <div class="flex items-center">
        <div class="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center mr-3">
          <i :class="['fa', category.icon, 'text-blue-600']"></i>
        </div>
        <div>
          <h3 class="font-medium text-gray-800">{{ category.name }}</h3>
          <p class="text-gray-500 text-xs mt-0.5">{{ category.count }} 篇文章</p>
        </div>
      </div>
      <i class="fa fa-arrow-right text-gray-400 transition-transform hover:text-blue-600 hover:translate-x-1"></i>
    </div>
    <p class="text-gray-600 text-sm mt-3 line-clamp-2">{{ category.description }}</p>
    <div class="text-xs text-gray-400 mt-3">更新于 {{ formatDate(category.lastUpdated) }}</div>
  </div>
</template>

<script>
export default {
  name: 'CategoryCard',
  props: {
    category: {
      type: Object,
      required: true
    }
  },
  methods: {
    filterByCategory(categoryName) {
      this.$emit('filter-by-category', categoryName)
    },
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' })
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