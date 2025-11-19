<template>
  <div class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
    <div class="bg-white rounded-lg shadow-lg w-full max-w-md">
      <!-- 模态框头部 -->
      <div class="flex justify-between items-center p-4 border-b border-gray-200">
        <h3 class="text-lg font-medium text-gray-800">{{ isEditing ? '编辑分类' : '新建分类' }}</h3>
        <button 
          class="text-gray-500 hover:text-gray-700"
          @click="$emit('close')"
        >
          <i class="fa fa-times"></i>
        </button>
      </div>
      
      <!-- 模态框内容 -->
      <div class="p-4">
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">分类名称</label>
          <input 
            v-model="categoryForm.name"
            type="text" 
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="请输入分类名称"
            maxlength="50"
          />
        </div>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">分类描述</label>
          <textarea 
            v-model="categoryForm.description"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
            placeholder="请输入分类描述"
            rows="3"
            maxlength="200"
          ></textarea>
        </div>
        
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 mb-2">选择图标</label>
          <div class="flex flex-wrap gap-2">
            <button 
              v-for="icon in availableIcons"
              :key="icon"
              :class="['w-10 h-10 rounded-full flex items-center justify-center transition-colors', categoryForm.icon === icon ? 'bg-blue-100 text-blue-600' : 'bg-gray-100 text-gray-600 hover:bg-gray-200']"
              @click="categoryForm.icon = icon"
              :title="icon"
            >
              <i :class="['fa', icon]"></i>
            </button>
          </div>
        </div>
      </div>
      
      <!-- 模态框底部 -->
      <div class="p-4 border-t border-gray-200 bg-gray-50">
        <div class="flex justify-end space-x-2">
          <button 
            class="px-3 py-1 border border-gray-300 rounded text-sm text-gray-700 hover:bg-gray-50 transition-colors"
            @click="$emit('close')"
          >
            取消
          </button>
          <button 
            class="px-3 py-1 bg-blue-600 text-white rounded text-sm hover:bg-blue-700 transition-colors"
            @click="saveCategory"
          >
            保存
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CategoryEditor',
  props: {
    category: {
      type: Object,
      default: null
    },
    availableIcons: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      categoryForm: {
        id: null,
        name: '',
        description: '',
        icon: 'fa-file-text-o'
      }
    }
  },
  computed: {
    isEditing() {
      return !!this.category
    }
  },
  watch: {
    category: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          this.categoryForm = { ...newVal }
        } else {
          this.resetForm()
        }
      }
    }
  },
  methods: {
    resetForm() {
      this.categoryForm = {
        id: null,
        name: '',
        description: '',
        icon: 'fa-file-text-o'
      }
    },
    saveCategory() {
      // 验证表单
      if (!this.categoryForm.name.trim()) {
        alert('请输入分类名称')
        return
      }
      if (!this.categoryForm.description.trim()) {
        alert('请输入分类描述')
        return
      }
      
      // 准备提交的数据
      const submitData = {
        ...this.categoryForm,
        // 如果是新建分类，添加创建日期和文章计数
        ...(!this.isEditing ? {
          count: 0,
          lastUpdated: new Date().toISOString().split('T')[0]
        } : {})
      }
      
      this.$emit('save', submitData)
    }
  }
}
</script>

<style scoped>
/* 分类编辑器样式已集成在组件中 */
</style>