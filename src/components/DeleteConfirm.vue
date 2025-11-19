<template>
  <div class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
    <div class="bg-white rounded-lg shadow-lg w-full max-w-sm">
      <!-- 模态框头部 -->
      <div class="p-4 border-b border-gray-200 flex items-center">
        <div class="w-8 h-8 rounded-full bg-red-100 flex items-center justify-center mr-3">
          <i class="fa fa-exclamation-triangle text-red-600"></i>
        </div>
        <h3 class="text-lg font-medium text-gray-800">确认删除</h3>
      </div>
      
      <!-- 模态框内容 -->
      <div class="p-4">
        <p class="text-gray-600 mb-4">{{ message }}</p>
      </div>
      
      <!-- 模态框底部 -->
      <div class="p-4 border-t border-gray-200 bg-gray-50">
        <div class="flex justify-end space-x-2">
          <button 
            class="px-3 py-1 border border-gray-300 rounded text-sm text-gray-700 hover:bg-gray-50 transition-colors"
            @click="$emit('cancel')"
          >
            取消
          </button>
          <button 
            class="px-3 py-1 bg-red-600 text-white rounded text-sm hover:bg-red-700 transition-colors"
            @click="$emit('confirm')"
          >
            确认删除
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DeleteConfirm',
  props: {
    message: {
      type: String,
      required: true
    }
  }
}
</script>

<style scoped>
/* 删除确认模态框样式已集成在组件中 */
</style>