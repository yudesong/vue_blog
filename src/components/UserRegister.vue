<template>
  <div class="flex justify-center items-center min-h-[70vh] py-12">
    <div class="w-full max-w-md bg-white rounded-xl shadow-lg overflow-hidden">
      <div class="p-8">
        <div class="text-center mb-8">
          <div class="flex justify-center mb-4">
            <i class="fa fa-user-plus text-indigo-600 text-4xl"></i>
          </div>
          <h2 class="text-2xl font-bold text-gray-900">创建账户</h2>
          <p class="text-gray-600 mt-2">加入我们的博客社区</p>
        </div>
        
        <form @submit.prevent="handleRegister" class="space-y-4">
          <!-- 用户名输入 -->
          <div>
            <label for="username" class="block text-sm font-medium text-gray-700 mb-1">用户名</label>
            <input
              id="username"
              v-model="form.username"
              type="text"
              required
              class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-colors"
              placeholder="请输入用户名"
              minlength="3"
              maxlength="30"
            >
            <div v-if="errors.username" class="text-red-500 text-xs mt-1">{{ errors.username }}</div>
          </div>
          
          <!-- 邮箱输入 -->
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 mb-1">邮箱</label>
            <input
              id="email"
              v-model="form.email"
              type="email"
              required
              class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-colors"
              placeholder="请输入邮箱地址"
            >
            <div v-if="errors.email" class="text-red-500 text-xs mt-1">{{ errors.email }}</div>
          </div>
          
          <!-- 密码输入 -->
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-1">密码</label>
            <input
              id="password"
              v-model="form.password"
              type="password"
              required
              class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-colors"
              placeholder="请输入密码"
              minlength="6"
            >
            <div v-if="errors.password" class="text-red-500 text-xs mt-1">{{ errors.password }}</div>
            <p class="text-gray-500 text-xs mt-1">密码至少包含6个字符</p>
          </div>
          
          <!-- 确认密码 -->
          <div>
            <label for="confirmPassword" class="block text-sm font-medium text-gray-700 mb-1">确认密码</label>
            <input
              id="confirmPassword"
              v-model="form.confirmPassword"
              type="password"
              required
              class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-colors"
              placeholder="请再次输入密码"
            >
            <div v-if="errors.confirmPassword" class="text-red-500 text-xs mt-1">{{ errors.confirmPassword }}</div>
          </div>
          
          <!-- 注册按钮 -->
          <button
            type="submit"
            :disabled="isSubmitting"
            class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2 px-4 rounded-md transition-colors flex justify-center items-center"
          >
            <span v-if="!isSubmitting">注册</span>
            <span v-else class="flex items-center">
              <i class="fa fa-spinner fa-spin mr-2"></i>
              注册中...
            </span>
          </button>
          
          <!-- 已有账户 -->
          <div class="text-center text-sm text-gray-600">
            已有账户？ <a href="#" @click.prevent="$emit('switchToLogin')" class="text-indigo-600 hover:text-indigo-700 font-medium">登录</a>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserRegister',
  emits: ['switchToLogin', 'registerSuccess'],
  data() {
    return {
      form: {
        username: '',
        email: '',
        password: '',
        confirmPassword: ''
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
      
      // 验证用户名
      if (!this.form.username.trim()) {
        this.errors.username = '用户名不能为空'
        isValid = false
      } else if (this.form.username.length < 3) {
        this.errors.username = '用户名至少需要3个字符'
        isValid = false
      }
      
      // 验证邮箱
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!this.form.email.trim()) {
        this.errors.email = '邮箱不能为空'
        isValid = false
      } else if (!emailRegex.test(this.form.email)) {
        this.errors.email = '请输入有效的邮箱地址'
        isValid = false
      }
      
      // 验证密码
      if (!this.form.password) {
        this.errors.password = '密码不能为空'
        isValid = false
      } else if (this.form.password.length < 6) {
        this.errors.password = '密码至少需要6个字符'
        isValid = false
      }
      
      // 验证确认密码
      if (!this.form.confirmPassword) {
        this.errors.confirmPassword = '请确认密码'
        isValid = false
      } else if (this.form.password !== this.form.confirmPassword) {
        this.errors.confirmPassword = '两次输入的密码不一致'
        isValid = false
      }
      
      return isValid
    },
    
    // 处理注册
    async handleRegister() {
      if (!this.validateForm()) {
        return
      }
      
      this.isSubmitting = true
      
      try {
        const response = await fetch('http://localhost:5000/api/auth/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            username: this.form.username,
            email: this.form.email,
            password: this.form.password
          })
        })
        
        const data = await response.json()
        
        if (!response.ok) {
          // 处理API返回的错误
          if (data.error) {
            if (data.error.includes('Username')) {
              this.errors.username = '用户名已存在'
            } else if (data.error.includes('Email')) {
              this.errors.email = '邮箱已存在'
            } else {
              alert('注册失败：' + data.error)
            }
          }
          return
        }
        
        // 注册成功
        this.$emit('registerSuccess', {
          id: data.id,
          username: this.form.username,
          email: this.form.email
        })
        
        // 重置表单
        this.form = {
          username: '',
          email: '',
          password: '',
          confirmPassword: ''
        }
        
        alert('注册成功！请登录')
        this.$emit('switchToLogin')
        
      } catch (error) {
        console.error('注册错误:', error)
        alert('注册失败，请稍后再试')
      } finally {
        this.isSubmitting = false
      }
    }
  }
}
</script>

<style scoped>
/* 可以添加一些特定的样式 */
input:focus {
  box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.2);
}

button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
</style>