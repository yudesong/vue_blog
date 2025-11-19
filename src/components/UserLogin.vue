<template>
  <div class="flex justify-center items-center min-h-[70vh] py-12">
    <div class="w-full max-w-md bg-white rounded-xl shadow-lg overflow-hidden">
      <div class="p-8">
        <div class="text-center mb-8">
          <div class="flex justify-center mb-4">
            <i class="fa fa-sign-in text-indigo-600 text-4xl"></i>
          </div>
          <h2 class="text-2xl font-bold text-gray-900">登录账户</h2>
          <p class="text-gray-600 mt-2">欢迎回来，请登录您的账户</p>
        </div>
        
        <form @submit.prevent="handleLogin" class="space-y-4">
          <!-- 用户名/邮箱输入 -->
          <div>
            <label for="loginInput" class="block text-sm font-medium text-gray-700 mb-1">用户名或邮箱</label>
            <input
              id="loginInput"
              v-model="form.loginInput"
              type="text"
              required
              class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-colors"
              placeholder="请输入用户名或邮箱"
            >
            <div v-if="errors.loginInput" class="text-red-500 text-xs mt-1">{{ errors.loginInput }}</div>
          </div>
          
          <!-- 密码输入 -->
          <div>
            <div class="flex justify-between items-center">
              <label for="password" class="block text-sm font-medium text-gray-700 mb-1">密码</label>
              <a href="#" class="text-xs text-indigo-600 hover:text-indigo-700 font-medium">忘记密码？</a>
            </div>
            <input
              id="password"
              v-model="form.password"
              type="password"
              required
              class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-colors"
              placeholder="请输入密码"
            >
            <div v-if="errors.password" class="text-red-500 text-xs mt-1">{{ errors.password }}</div>
          </div>
          
          <!-- 记住我 -->
          <div class="flex items-center">
            <input
              id="rememberMe"
              v-model="form.rememberMe"
              type="checkbox"
              class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
            >
            <label for="rememberMe" class="ml-2 block text-sm text-gray-700">记住我</label>
          </div>
          
          <!-- 登录按钮 -->
          <button
            type="submit"
            :disabled="isSubmitting"
            class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2 px-4 rounded-md transition-colors flex justify-center items-center"
          >
            <span v-if="!isSubmitting">登录</span>
            <span v-else class="flex items-center">
              <i class="fa fa-spinner fa-spin mr-2"></i>
              登录中...
            </span>
          </button>
          
          <!-- 没有账户 -->
          <div class="text-center text-sm text-gray-600">
            没有账户？ <a href="#" @click.prevent="$emit('switchToRegister')" class="text-indigo-600 hover:text-indigo-700 font-medium">注册</a>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserLogin',
  emits: ['switchToRegister', 'loginSuccess'],
  data() {
    return {
      form: {
        loginInput: '',
        password: '',
        rememberMe: false
      },
      errors: {},
      isSubmitting: false
    }
  },
  methods: {
    // 表单验证
    validateForm() {
      this.errors = {}
      let isValid = true
      
      // 验证登录输入
      if (!this.form.loginInput.trim()) {
        this.errors.loginInput = '请输入用户名或邮箱'
        isValid = false
      }
      
      // 验证密码
      if (!this.form.password) {
        this.errors.password = '请输入密码'
        isValid = false
      }
      
      return isValid
    },
    
    // 处理登录
    async handleLogin() {
      if (!this.validateForm()) {
        return
      }
      
      this.isSubmitting = true
      
      try {
        const response = await fetch('http://localhost:5000/api/auth/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            username: this.form.loginInput,  // 后端目前只接受username参数，我们传入loginInput
            password: this.form.password
          })
        })
        
        const data = await response.json()
        
        if (!response.ok) {
          // 处理登录失败
          if (data.error) {
            alert('登录失败：' + data.error)
          }
          return
        }
        
        // 登录成功，保存用户信息
        const userData = {
          id: data.id,
          username: data.username,
          email: data.email,
          isAdmin: data.isAdmin,
          token: data.token
        }
        
        // 如果选择记住我，保存到localStorage，否则保存到sessionStorage
        const storage = this.form.rememberMe ? localStorage : sessionStorage
        storage.setItem('user', JSON.stringify(userData))
        
        // 触发登录成功事件
        this.$emit('loginSuccess', userData)
        
        // 显示成功消息
        alert('登录成功！')
        
        // 重置表单
        this.form = {
          loginInput: '',
          password: '',
          rememberMe: false
        }
        
        // 可以在这里跳转到首页或其他页面
        this.$parent.switchView('home')
        
      } catch (error) {
        console.error('登录错误:', error)
        alert('登录失败，请稍后再试')
      } finally {
        this.isSubmitting = false
      }
    }
  }
}
</script>

<style scoped>
input:focus {
  box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.2);
}

button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
</style>