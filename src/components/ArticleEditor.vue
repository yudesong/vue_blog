<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-5xl mx-auto p-4 bg-white min-h-screen">
      <!-- 模态框头部 -->
      <div class="flex justify-between items-center p-4 border-b border-gray-200">
        <h3 class="text-lg font-medium text-gray-800">{{ isEditing ? '编辑文章' : '新建文章' }}</h3>
        <div class="flex space-x-2">
          <button 
            class="px-3 py-1 border border-gray-300 rounded text-sm text-gray-700 hover:bg-gray-50 transition-colors"
            @click="$emit('close')"
          >
            取消
          </button>
          <button 
            class="px-3 py-1 bg-blue-600 text-white rounded text-sm hover:bg-blue-700 transition-colors"
            @click="saveArticle"
          >
            保存
          </button>
        </div>
      </div>
      
      <!-- 模态框内容 -->
      <div class="flex-1 overflow-y-auto p-4">
        <!-- 文章基本信息 -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div class="md:col-span-2">
            <label class="block text-sm font-medium text-gray-700 mb-1">文章标题</label>
            <input 
              v-model="articleForm.title"
              type="text" 
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="请输入文章标题"
              maxlength="100"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">文章分类</label>
            <select 
              v-model="articleForm.category_id"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">请选择分类</option>
              <option v-for="category in categories" :key="category.id" :value="category.id">
                {{ category.name }}
              </option>
            </select>
          </div>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">文章标签</label>
            <input 
              v-model="articleForm.tagsStr"
              type="text" 
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="多个标签用逗号分隔"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">发布日期</label>
            <input 
              v-model="articleForm.publishedDate"
              type="date" 
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
        
        <!-- 特色图片 -->
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 mb-2">特色图片</label>
          <div class="flex items-center space-x-4">
            <div v-if="articleForm.coverImage" class="w-32 h-20 rounded overflow-hidden border border-gray-200">
              <img :src="articleForm.coverImage" alt="封面图片" class="w-full h-full object-cover" />
            </div>
            <button 
              class="px-3 py-1 border border-gray-300 rounded text-sm text-gray-700 hover:bg-gray-50 transition-colors flex items-center"
              @click="triggerImageUpload"
            >
              <i class="fa fa-upload mr-1"></i>
              上传图片
            </button>
            <input 
              ref="imageUpload"
              type="file" 
              accept="image/*"
              class="hidden"
              @change="handleCoverImageUpload"
            />
          </div>
        </div>
        
        <!-- 文章内容编辑器 -->
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 mb-2">文章内容</label>
          
          <!-- 编辑器工具栏 -->
          <div class="border border-gray-300 rounded-t-lg p-2 bg-gray-50 flex flex-wrap gap-1">
            <button class="p-1 hover:bg-gray-200 rounded" title="加粗" @click="formatText('bold')"><i class="fa fa-bold"></i></button>
            <button class="p-1 hover:bg-gray-200 rounded" title="斜体" @click="formatText('italic')"><i class="fa fa-italic"></i></button>
            <button class="p-1 hover:bg-gray-200 rounded" title="下划线" @click="formatText('underline')"><i class="fa fa-underline"></i></button>
            <span class="border-r border-gray-300 h-6 mx-1"></span>
            <button class="p-1 hover:bg-gray-200 rounded" title="H2标题" @click="formatText('formatBlock', 'h2')"><i class="fa fa-header"></i>H2</button>
            <button class="p-1 hover:bg-gray-200 rounded" title="H3标题" @click="formatText('formatBlock', 'h3')"><i class="fa fa-header"></i>H3</button>
            <span class="border-r border-gray-300 h-6 mx-1"></span>
            <button class="p-1 hover:bg-gray-200 rounded" title="无序列表" @click="formatText('insertUnorderedList')"><i class="fa fa-list-ul"></i></button>
            <button class="p-1 hover:bg-gray-200 rounded" title="有序列表" @click="formatText('insertOrderedList')"><i class="fa fa-list-ol"></i></button>
            <span class="border-r border-gray-300 h-6 mx-1"></span>
            <button class="p-1 hover:bg-gray-200 rounded" title="插入链接" @click="insertLink"><i class="fa fa-link"></i></button>
            <button class="p-1 hover:bg-gray-200 rounded" title="插入图片" @click="triggerImageInsert"><i class="fa fa-image"></i></button>
            <button class="p-1 hover:bg-gray-200 rounded" title="插入视频" @click="insertVideo"><i class="fa fa-video"></i></button>
            <button class="p-1 hover:bg-gray-200 rounded" title="插入代码块" @click="insertCodeBlock"><i class="fa fa-code"></i></button>
          </div>
          
          <!-- 编辑器内容区 -->
          <div 
            ref="editorContent"
            contenteditable="true"
            class="border border-gray-300 border-t-0 rounded-b-lg p-4 min-h-[300px] focus:outline-none focus:ring-2 focus:ring-blue-500"
            @input="updateContent"
          ></div>
        </div>
        
        <!-- 媒体上传区域 -->
        <div class="mb-4" v-if="articleForm.media.length > 0">
          <label class="block text-sm font-medium text-gray-700 mb-2">上传的媒体</label>
          <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-2">
            <div v-for="media in articleForm.media" :key="media.id" class="relative">
              <div class="bg-gray-100 rounded p-2 flex flex-col items-center justify-center">
                <i v-if="media.type === 'video'" class="fa fa-video text-gray-500 text-2xl mb-1"></i>
                <i v-else-if="media.type === 'audio'" class="fa fa-music text-gray-500 text-2xl mb-1"></i>
                <img v-else :src="media.url" alt="媒体预览" class="w-full h-20 object-cover rounded mb-1" />
                <div class="text-xs text-gray-500 truncate text-center">{{ media.name }}</div>
              </div>
              <button 
                class="absolute top-1 right-1 w-5 h-5 bg-red-500 text-white rounded-full flex items-center justify-center hover:bg-red-600 transition-colors"
                @click="removeMedia(media.id)"
              >
                <i class="fa fa-times text-xs"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 页面底部操作区 -->
      <div class="fixed bottom-0 left-0 right-0 p-4 border-t border-gray-200 bg-white shadow-lg">
        <div class="max-w-5xl mx-auto flex justify-between items-center">
          <div class="text-sm text-gray-500">
            字数统计：{{ contentWordCount }}
          </div>
          <div>
            <button 
              class="px-4 py-2 border border-gray-300 text-gray-700 rounded hover:bg-gray-100 mr-2 transition-colors"
              @click="cancelEdit"
            >
              取消
            </button>
            <button 
              class="px-4 py-2 border border-gray-300 text-gray-700 rounded hover:bg-gray-100 mr-2 transition-colors"
              @click="saveAsDraft"
            >
              保存为草稿
            </button>
            <button 
              class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
              @click="publishArticle"
            >
              {{ isEditing ? '更新文章' : '发布文章' }}
            </button>
          </div>
        </div>
      </div>
      
      <!-- 隐藏的文件上传输入 -->
      <input 
        ref="imageInsert"
        type="file" 
        accept="image/*"
        class="hidden"
        @change="handleImageUpload"
      />
      <input 
        ref="videoUpload"
        type="file" 
        accept="video/*"
        class="hidden"
        @change="handleVideoUpload"
      />
      <input 
        ref="audioUpload"
        type="file" 
        accept="audio/*"
        class="hidden"
        @change="handleAudioUpload"
      />
    </div>
  </div>
</template>

<script>
import hljs from 'highlight.js';
import 'highlight.js/styles/atom-one-dark.css';

export default {
  name: 'ArticleEditor',
  props: {
    article: {
      type: Object,
      default: null
    },
    categories: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      // 代码语言列表
      codeLanguages: [
        { value: 'javascript', label: 'JavaScript' },
        { value: 'python', label: 'Python' },
        { value: 'java', label: 'Java' },
        { value: 'cpp', label: 'C++' },
        { value: 'c', label: 'C' },
        { value: 'csharp', label: 'C#' },
        { value: 'php', label: 'PHP' },
        { value: 'ruby', label: 'Ruby' },
        { value: 'go', label: 'Go' },
        { value: 'rust', label: 'Rust' },
        { value: 'typescript', label: 'TypeScript' },
        { value: 'html', label: 'HTML' },
        { value: 'css', label: 'CSS' },
        { value: 'json', label: 'JSON' },
        { value: 'xml', label: 'XML' },
        { value: 'sql', label: 'SQL' },
        { value: 'bash', label: 'Bash' },
        { value: 'yaml', label: 'YAML' },
        { value: 'markdown', label: 'Markdown' },
        { value: 'plaintext', label: '纯文本' }
      ],
      articleForm: {
        id: null,
        title: '',
        category_id: '', // 修改为与watch中一致的字段名
        tagsStr: '',
        coverImage: '',
        content: '',
        status: 'published',
        publishedDate: '',
        media: []
      }
    }
  },
  computed: {
    isEditing() {
      return !!this.article
    },
    contentWordCount() {
      const plainText = this.articleForm.content.replace(/<[^>]*>/g, '').replace(/&nbsp;/g, ' ')
      return plainText.trim().length
    }
  },
    watch: {
      article: {
        immediate: true,
        handler(newVal) {
          if (newVal) {
            // 根据文章分类名称查找对应的分类ID
            const categoryId = this.categories.find(c => c.name === newVal.category)?.id || '';
            
            this.articleForm = {
              id: newVal.id,
              title: newVal.title,
              category_id: categoryId,
              tagsStr: newVal.tags.join(','),
              coverImage: newVal.coverImage,
              content: newVal.content || '<p></p>',
              status: 'published',
              publishedDate: this.formatDateForInput(new Date(newVal.publishedDate)),
              media: []
            }
          } else {
            this.resetForm()
          }
        }
      },
      // 监听articleForm.content变化，确保编辑器内容同步
      'articleForm.content': {
        handler(newContent) {
          // 只有当编辑器内容与新内容不同时才更新，避免用户输入时的循环更新
          if (this.$refs.editorContent && this.$refs.editorContent.innerHTML !== newContent) {
            this.$nextTick(() => {
              if (this.$refs.editorContent) {
                this.$refs.editorContent.innerHTML = newContent;
                // 应用代码高亮
                this.applyHighlight();
              }
            });
          }
        },
        // 不要设置immediate，避免与mounted中的初始化冲突
      }
    },
  mounted() {
    if (!this.isEditing) {
      this.resetForm()
    } else {
      // 使用nextTick确保DOM渲染完成
      this.$nextTick(() => {
        if (this.$refs.editorContent) {
          this.$refs.editorContent.innerHTML = this.articleForm.content || '<p></p>';
          // 应用代码高亮
          this.applyHighlight();
        }
      })
    }
    
    // 添加粘贴事件监听
    if (this.$refs.editorContent) {
      this.$refs.editorContent.addEventListener('paste', this.handlePaste);
      // 添加键盘事件监听，特别是删除键
      this.$refs.editorContent.addEventListener('keydown', this.handleKeydown);
      // 设置代码变化观察器
      this.observeCodeChanges();
    }
  },
  
  beforeUnmount() {
    // 移除事件监听
    if (this.$refs.editorContent) {
      this.$refs.editorContent.removeEventListener('paste', this.handlePaste);
      this.$refs.editorContent.removeEventListener('keydown', this.handleKeydown);
    }
    
    // 清理mutation observer
    if (this._codeObserver) {
      this._codeObserver.disconnect();
    }
  },
  methods: {
    // 取消编辑
    cancelEdit() {
      if (confirm('确定要取消编辑吗？未保存的内容将丢失。')) {
        this.$emit('cancel')
      }
    },
    
    resetForm() {
      this.articleForm = {
        id: null,
        title: '',
        category_id: '', // 确保这里也是正确的字段名
        tagsStr: '',
        coverImage: '',
        content: '<p>开始撰写您的文章内容...</p>',
        status: 'published',
        publishedDate: this.formatDateForInput(new Date()),
        media: []
      }
      
      // 使用nextTick确保DOM渲染完成
      this.$nextTick(() => {
        if (this.$refs.editorContent) {
          this.$refs.editorContent.innerHTML = this.articleForm.content;
        }
      });
    },
    
    // 处理粘贴事件
    async handlePaste(event) {
      // 阻止默认粘贴行为
      event.preventDefault();
      
      console.log('粘贴事件触发');
      
      // 获取粘贴的内容
      const clipboardData = event.clipboardData || window.clipboardData;
      let html = clipboardData.getData('text/html');
      
      if (html) {
        console.log('检测到HTML内容');
        // 创建临时DOM元素来处理HTML
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = html;
        
        // 检查是否包含代码块，如果有，尝试添加语言类
        const codeBlocks = tempDiv.querySelectorAll('pre code');
        if (codeBlocks.length > 0) {
          codeBlocks.forEach(block => {
            // 如果代码块没有语言类，添加默认的language-plaintext类
            if (!Array.from(block.classList).some(cls => cls.startsWith('language-'))) {
              block.classList.add('language-plaintext');
            }
          });
        }
        
        // 查找所有图片元素
        const images = tempDiv.querySelectorAll('img');
        console.log(`找到 ${images.length} 张图片`);
        
        if (images.length > 0) {
          const imagePromises = [];
          
          // 对每个图片进行处理
          images.forEach((img, index) => {
            let src = img.src;
            // 检查是否有data-src或其他可能的图片源属性
            if (!src || src === 'about:blank') {
              src = img.getAttribute('data-src') || img.getAttribute('data-ratio') || img.src;
            }
            
            console.log(`处理图片 ${index + 1}: ${src}`);
            
            if (src && !src.startsWith('data:')) {
              // 为每个图片创建一个Promise
              const promise = this.convertImageToDataURL(src).then(dataURL => {
                console.log(`图片 ${index + 1} 转换成功`);
                // 替换图片src为DataURL
                img.src = dataURL;
                img.srcset = ''; // 清空srcset以避免冲突
                // 移除可能导致问题的属性
                img.removeAttribute('data-src');
                img.removeAttribute('data-w');
                img.removeAttribute('data-ratio');
                img.removeAttribute('data-type');
                // 添加适当的样式
                img.classList.add('max-w-full', 'h-auto');
                return dataURL;
              }).catch(error => {
                console.error(`图片 ${index + 1} 转换失败:`, src, error);
                // 如果转换失败，尝试更简单的方法
                try {
                  // 直接使用fetch获取图片
                  return fetch(src, {
                    mode: 'cors',
                    headers: {
                      'Access-Control-Allow-Origin': '*'
                    },
                    credentials: 'include'
                  })
                  .then(response => {
                    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
                    return response.blob();
                  })
                  .then(blob => {
                    const reader = new FileReader();
                    return new Promise((resolve) => {
                      reader.onloadend = () => {
                        const fallbackDataURL = reader.result;
                        img.src = fallbackDataURL;
                        console.log(`图片 ${index + 1} 使用备用方法成功`);
                        resolve(fallbackDataURL);
                      };
                      reader.readAsDataURL(blob);
                    });
                  })
                  .catch(fallbackError => {
                    console.error(`图片 ${index + 1} 备用方法也失败:`, fallbackError);
                    // 最后的选择 - 使用占位图
                    img.src = 'https://picsum.photos/800/400';
                    img.alt = '图片加载失败，使用占位图';
                    return null;
                  });
                } catch (e) {
                  img.src = 'https://picsum.photos/800/400';
                  return null;
                }
              });
              imagePromises.push(promise);
            }
          });
          
          // 等待所有图片处理完成
          await Promise.all(imagePromises);
          console.log('所有图片处理完成');
        }
        
        // 获取处理后的HTML
        const processedHtml = tempDiv.innerHTML;
        console.log('处理后的HTML内容:', processedHtml.substring(0, 100) + '...');
        
        // 插入到编辑器
        this.formatText('insertHTML', processedHtml);
        
        // 应用代码高亮
        this.applyHighlight();
      } else {
        // 如果没有HTML内容，只粘贴纯文本
        const text = clipboardData.getData('text/plain');
        if (text) {
          console.log('粘贴纯文本内容');
          this.formatText('insertText', text);
        }
      }
    },
    
    // 将图片URL转换为DataURL
    convertImageToDataURL(url) {
      return new Promise((resolve, reject) => {
        // 首先尝试直接fetch获取图片（更可靠的方法）
        fetch(url, {
          mode: 'cors',
          headers: {
            'Content-Type': 'image/jpeg',
            'Access-Control-Allow-Origin': '*'
          },
          credentials: 'include'
        })
        .then(response => {
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          return response.blob();
        })
        .then(blob => {
          const reader = new FileReader();
          reader.onloadend = () => {
            console.log('使用fetch成功获取图片并转换为DataURL');
            resolve(reader.result);
          };
          reader.onerror = () => {
            console.error('FileReader读取失败');
            reject(new Error('读取图片失败'));
          };
          reader.readAsDataURL(blob);
        })
        .catch(fetchError => {
          console.warn('fetch方法失败，尝试使用canvas方法:', fetchError);
          
          // 如果fetch失败，尝试使用canvas方法
          try {
            // 创建一个新的图片对象
            const img = new Image();
            
            // 设置CORS以允许跨域图片
            img.crossOrigin = 'anonymous';
            
            img.onload = function() {
              try {
                // 创建canvas元素
                const canvas = document.createElement('canvas');
                canvas.width = this.width || 800;
                canvas.height = this.height || 600;
                
                // 绘制图片到canvas
                const ctx = canvas.getContext('2d');
                ctx.drawImage(this, 0, 0, canvas.width, canvas.height);
                
                try {
                  // 转换为DataURL
                  const dataURL = canvas.toDataURL('image/jpeg', 0.9);
                  console.log('使用canvas成功转换图片');
                  resolve(dataURL);
                } catch (toDataURLError) {
                  console.error('canvas toDataURL失败:', toDataURLError);
                  reject(toDataURLError);
                }
              } catch (canvasError) {
                console.error('canvas处理失败:', canvasError);
                reject(canvasError);
              }
            };
            
            img.onerror = function() {
              console.error('图片加载失败');
              reject(new Error('图片加载失败'));
            };
            
            // 设置超时
            setTimeout(() => {
              if (!img.complete) {
                img.src = '';
                reject(new Error('图片加载超时'));
              }
            }, 10000);
            
            // 开始加载图片
            img.src = url;
          } catch (error) {
            reject(error);
          }
        });
      });
    },
    
    // 富文本编辑核心方法
    formatText(command, value = null) {
      // 先确保编辑器获得焦点
      if (this.$refs.editorContent) {
        this.$refs.editorContent.focus();
        
        // 尝试执行命令
        try {
          // 对于formatBlock命令，需要特殊处理
          if (command === 'formatBlock' && value) {
            document.execCommand('formatBlock', false, `<${value}>`);
          } else {
            document.execCommand(command, false, value);
          }
          this.updateContent();
        } catch (error) {
          console.error('编辑器命令执行失败:', error);
        }
      }
    },
    
    // 插入链接
    insertLink() {
      const url = prompt('请输入链接地址:', 'http://');
      if (url) {
        this.formatText('createLink', url);
      }
    },
    
    // 插入视频
    insertVideo() {
      const url = prompt('请输入视频地址:', 'http://');
      if (url) {
        this.formatText('insertHTML', `<video controls width="100%" src="${url}"></video>`);
      }
    },
    
    // 插入代码块
    insertCodeBlock() {
      // 创建一个临时的div来显示语言选择对话框
      const dialogContainer = document.createElement('div');
      dialogContainer.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
      dialogContainer.innerHTML = `
        <div class="bg-white p-4 rounded-lg shadow-lg max-w-md w-full">
          <h3 class="text-lg font-medium mb-4">选择编程语言</h3>
          <select id="codeLanguageSelect" class="w-full p-2 border border-gray-300 rounded mb-4">
            ${this.codeLanguages.map(lang => `
              <option value="${lang.value}">${lang.label}</option>
            `).join('')}
          </select>
          <div class="flex justify-end space-x-2">
            <button id="cancelBtn" class="px-4 py-2 border border-gray-300 rounded">取消</button>
            <button id="confirmBtn" class="px-4 py-2 bg-blue-600 text-white rounded">确定</button>
          </div>
        </div>
      `;
      
      document.body.appendChild(dialogContainer);
      
      const select = dialogContainer.querySelector('#codeLanguageSelect');
      const cancelBtn = dialogContainer.querySelector('#cancelBtn');
      const confirmBtn = dialogContainer.querySelector('#confirmBtn');
      
      // 确认按钮点击事件
      confirmBtn.addEventListener('click', () => {
        const language = select.value;
        const languageClass = language === 'plaintext' ? '' : `language-${language}`;
        
        // 插入代码块
        this.formatText('insertHTML', `<pre><code class="${languageClass}">在这里输入代码...</code></pre>`);
        
        // 应用代码高亮
        this.highlightAllCode();
        
        // 清理对话框
        document.body.removeChild(dialogContainer);
        
        // 尝试聚焦到代码块并选择占位文本
        setTimeout(() => {
          const codeElements = this.$refs.editorContent.querySelectorAll('pre code');
          const lastCode = codeElements[codeElements.length - 1];
          if (lastCode && lastCode.textContent === '在这里输入代码...') {
            const range = document.createRange();
            range.selectNodeContents(lastCode);
            const selection = window.getSelection();
            selection.removeAllRanges();
            selection.addRange(range);
          }
        }, 0);
      });
      
      // 取消按钮点击事件
      cancelBtn.addEventListener('click', () => {
        document.body.removeChild(dialogContainer);
      });
    },
    
    // 处理键盘事件，特别是删除键
    handleKeydown(event) {
      // 阻止删除键可能导致的页面导航行为
      if (event.key === 'Backspace' || event.key === 'Delete') {
        // 阻止默认的页面导航行为
        event.stopPropagation();
        
        // 确保编辑器内容区域获得焦点
        if (this.$refs.editorContent) {
          // 检查当前选中内容
          const selection = window.getSelection();
          if (selection.rangeCount > 0) {
            const range = selection.getRangeAt(0);
            
            // 如果删除空内容或光标在开始位置，防止可能的页面跳转
            if (range.startOffset === 0 && range.endOffset === 0 && range.startContainer.nodeType === 3) {
              // 如果是文本节点的开头，确保不会触发任何特殊行为
              const parentElement = range.startContainer.parentNode;
              if (parentElement && parentElement.previousSibling === null) {
                // 在顶级元素的开头，确保不会触发任何页面级导航
                event.preventDefault();
                
                // 手动处理删除操作
                if (parentElement.textContent.trim() === '' && parentElement.tagName.toLowerCase() === 'p') {
                  // 保留空段落，防止编辑器内容完全清空
                  return;
                }
                
                // 恢复默认行为，允许删除
                setTimeout(() => {
                  document.execCommand('delete', false, null);
                  this.updateContent();
                }, 0);
              }
            }
          }
        }
      }
    },
    
    // 应用代码高亮并添加复制按钮
    highlightAllCode() {
      if (this.$refs.editorContent) {
        const codeBlocks = this.$refs.editorContent.querySelectorAll('pre code');
        codeBlocks.forEach(block => {
          // 先应用高亮
          this.applyHighlightToBlock(block);
          
          // 为代码块添加复制按钮
          this.addCopyButtonToBlock(block);
        });
      }
    },
    
    // 只重新高亮代码内容，不重复添加复制按钮
    rehighlightCodeWithoutButtons() {
      if (this.$refs.editorContent) {
        const codeBlocks = this.$refs.editorContent.querySelectorAll('pre code');
        codeBlocks.forEach(block => {
          this.applyHighlightToBlock(block);
        });
      }
    },
    
    // 应用高亮到单个代码块
    applyHighlightToBlock(block) {
      // 检查是否需要重新高亮（内容变化时）
      if (!block.classList.contains('hljs') || this.needsRehighlight(block)) {
        // 获取语言类
        const languageClass = Array.from(block.classList).find(cls => cls.startsWith('language-'));
        if (languageClass) {
          const language = languageClass.replace('language-', '');
          // 尝试使用指定语言高亮
          if (hljs.getLanguage(language)) {
            hljs.highlightElement(block);
          } else {
            // 如果指定的语言不可用，自动检测
            hljs.highlightElement(block);
          }
        } else {
          // 自动检测语言
          hljs.highlightElement(block);
        }
      }
    },
    
    // 判断代码块是否需要重新高亮
    needsRehighlight(block) {
      // 简单判断：如果代码块的子节点只有文本节点，可能需要重新高亮
      // 或者我们可以添加一个时间戳标记上次高亮时间
      return Array.from(block.childNodes).some(node => node.nodeType === 3);
    },
    
    // 为代码块添加复制按钮
    addCopyButtonToBlock(block) {
      const preElement = block.parentElement;
      // 检查是否已经有复制按钮，避免重复添加
      if (preElement && !preElement.querySelector('.copy-button')) {
        // 创建复制按钮
        const copyButton = document.createElement('button');
        copyButton.className = 'copy-button';
        copyButton.innerHTML = '<i class="fa fa-copy"></i>';
        copyButton.title = '复制代码';
        copyButton.addEventListener('click', (e) => {
          e.stopPropagation();
          this.copyCode(block.textContent);
          // 临时更改按钮文本为"已复制"
          const originalText = copyButton.innerHTML;
          copyButton.innerHTML = '<i class="fa fa-check"></i>';
          setTimeout(() => {
            copyButton.innerHTML = originalText;
          }, 2000);
        });
        
        // 确保pre元素有相对定位
        if (window.getComputedStyle(preElement).position === 'static') {
          preElement.style.position = 'relative';
        }
        
        // 添加按钮到pre元素
        preElement.appendChild(copyButton);
      }
    },
    
    // 复制代码功能
    copyCode(text) {
      navigator.clipboard.writeText(text).then(() => {
        // 可以添加复制成功的提示
        this.showNotification('代码已复制到剪贴板');
      }).catch(err => {
        console.error('复制失败:', err);
      });
    },
    
    // 显示通知提示
    showNotification(message) {
      // 创建通知元素
      const notification = document.createElement('div');
      notification.className = 'code-copy-notification';
      notification.textContent = message;
      
      // 添加到文档
      document.body.appendChild(notification);
      
      // 3秒后移除
      setTimeout(() => {
        notification.classList.add('fade-out');
        setTimeout(() => {
          document.body.removeChild(notification);
        }, 300);
      }, 2000);
    },
    
    // 监听代码块变化并重新高亮
    observeCodeChanges() {
      if (this.$refs.editorContent) {
        const observer = new MutationObserver(mutations => {
          let needsHighlight = false;
          
          mutations.forEach(mutation => {
            // 检查是否有代码块被修改或添加
            const relevantChange = Array.from(mutation.addedNodes).some(node => {
              if (node.nodeType === 1) {
                // 检查是否是pre元素或包含pre code的元素
                return node.tagName === 'PRE' || 
                       (node.querySelector && node.querySelector('pre code')) ||
                       (node.parentElement && node.parentElement.tagName === 'PRE' && node.tagName === 'CODE');
              }
              return false;
            });
            
            // 检查文本内容变化，可能是代码内容修改
            const textChangeInCode = mutation.type === 'characterData' && 
                                     mutation.target.parentElement &&
                                     mutation.target.parentElement.tagName === 'CODE' &&
                                     mutation.target.parentElement.parentElement &&
                                     mutation.target.parentElement.parentElement.tagName === 'PRE';
            
            if (relevantChange || textChangeInCode) {
              needsHighlight = true;
            }
          });
          
          if (needsHighlight) {
            // 延迟执行以确保DOM完全更新
            setTimeout(() => {
              // 只重新高亮内容，不重复添加复制按钮
              this.rehighlightCodeWithoutButtons();
            }, 0);
          }
        });
        
        observer.observe(this.$refs.editorContent, {
          childList: true,
          subtree: true,
          characterData: true
        });
        
        // 保存observer引用以便在组件销毁时清理
        this._codeObserver = observer;
      }
    },
    
    // 手动应用代码高亮（用于粘贴或内容加载后）
    applyHighlight() {
      // 只重新高亮代码内容，不添加复制按钮
      setTimeout(() => this.rehighlightCodeWithoutButtons(), 0);
    },
    formatDateForInput(date) {
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      return `${year}-${month}-${day}`
    },
    updateContent() {
      if (this.$refs.editorContent) {
        // 保存当前光标位置
        const selection = window.getSelection();
        const range = selection.rangeCount > 0 ? selection.getRangeAt(0) : null;
        
        // 获取当前的代码块数量，用于后续检查是否有新的代码块被添加
        const currentCodeBlocks = this.$refs.editorContent.querySelectorAll('pre code');
        const currentBlockCount = currentCodeBlocks.length;
        
        // 更新内容
        this.articleForm.content = this.$refs.editorContent.innerHTML;
        
        // 先应用代码高亮
        this.applyHighlight();
        
        // 检查是否有新的代码块被添加，如果有，则为新代码块添加复制按钮
        setTimeout(() => {
          const updatedCodeBlocks = this.$refs.editorContent.querySelectorAll('pre code');
          if (updatedCodeBlocks.length > currentBlockCount) {
            // 只为新添加的代码块添加复制按钮
            const newBlocks = Array.from(updatedCodeBlocks).slice(currentBlockCount);
            newBlocks.forEach(block => {
              this.addCopyButtonToBlock(block);
            });
          }
        }, 10);
        
        // 恢复光标位置（如果之前有有效光标位置）
        setTimeout(() => {
          if (range && selection) {
            try {
              selection.removeAllRanges();
              selection.addRange(range);
            } catch (e) {
              // 忽略无法恢复光标的情况
            }
          }
        }, 0);
      }
    },
    
    // 触发特色图片上传
    triggerImageUpload() {
      this.$refs.imageUpload.click()
    },
    
    // 触发内容中插入图片
    triggerImageInsert() {
      this.$refs.imageInsert.click()
    },
    
    // 处理特色图片上传
    handleCoverImageUpload(e) {
      const file = e.target.files[0]
      if (file) {
        // 这里只是模拟上传，实际项目中应该发送到服务器
        const reader = new FileReader()
        reader.onload = (event) => {
          this.articleForm.coverImage = event.target.result
        }
        reader.readAsDataURL(file)
      }
      // 重置input，允许重复上传同一文件
      e.target.value = ''
    },
    
    // 处理内容图片上传
    handleImageUpload(e) {
      const file = e.target.files[0]
      if (file) {
        // 模拟上传
        const reader = new FileReader()
        reader.onload = (event) => {
          // 将图片添加到媒体列表
          this.articleForm.media.push({
            id: Date.now(),
            type: 'image',
            url: event.target.result,
            name: file.name
          })
          
          // 同时在编辑器中插入图片
          if (this.$refs.editorContent) {
            this.$refs.editorContent.focus()
            this.formatText('insertHTML', `<img src="${event.target.result}" alt="${file.name}" class="max-w-full h-auto">`)
          }
        }
        reader.readAsDataURL(file)
      }
      // 重置input，允许重复上传同一文件
      e.target.value = ''
    },
    
    // 处理视频上传
    handleVideoUpload(e) {
      const file = e.target.files[0]
      if (file) {
        // 模拟上传
        this.articleForm.media.push({
          id: Date.now(),
          type: 'video',
          url: '#',
          name: file.name
        })
      }
      e.target.value = ''
    },
    
    // 处理音频上传
    handleAudioUpload(e) {
      const file = e.target.files[0]
      if (file) {
        // 模拟上传
        this.articleForm.media.push({
          id: Date.now(),
          type: 'audio',
          url: '#',
          name: file.name
        })
      }
      e.target.value = ''
    },
    
    // 移除媒体
    removeMedia(id) {
      this.articleForm.media = this.articleForm.media.filter(media => media.id !== id)
    },
    // 简化版保存草稿方法
    saveAsDraft() {
      console.log('开始保存草稿')
      
      // 简化验证
      if (!this.articleForm.title.trim()) {
        alert('请输入文章标题')
        return
      }
      
      // 准备提交数据
      const submitData = {
        id: this.articleForm.id,
        title: this.articleForm.title,
        category_id: this.articleForm.category_id,
        content: this.articleForm.content,
        status: 'draft',
        publishedDate: this.articleForm.publishedDate,
        coverImage: this.articleForm.coverImage,
        tags: this.articleForm.tagsStr.split(',').map(tag => tag.trim()).filter(tag => tag)
      }
      
      console.log('发出save事件（草稿）:', submitData)
      
      // 直接使用this.$emit
      this.$emit('save', submitData)
      console.log('save事件已发出')
      alert('文章已保存为草稿')
    },
    
    // 简化版发布/更新方法
    publishArticle() {
      console.log('开始发布/更新文章')
      
      // 完整验证
      if (!this.articleForm.title.trim()) {
        alert('请输入文章标题')
        return
      }
      if (!this.articleForm.category_id) {
        alert('请选择文章分类')
        return
      }
      if (!this.articleForm.content.trim() || this.articleForm.content === '<p>开始撰写您的文章内容...</p>') {
        alert('请输入文章内容')
        return
      }
      
      // 准备提交数据
      const submitData = {
        id: this.articleForm.id,
        title: this.articleForm.title,
        category_id: this.articleForm.category_id,
        content: this.articleForm.content,
        status: 'published',
        publishedDate: new Date().toISOString(),
        coverImage: this.articleForm.coverImage,
        tags: this.articleForm.tagsStr.split(',').map(tag => tag.trim()).filter(tag => tag)
      }
      
      console.log('发出save事件（发布）:', submitData)
      
      // 直接使用this.$emit
      this.$emit('save', submitData)
      console.log('save事件已发出')
      alert('文章已成功' + (this.isEditing ? '更新' : '发布'))
    },
     // 更新文章
    async updateArticle() {
      if (!this.articleForm.id) {
        alert('请先编辑文章');
        return;
      }
      
      // 转换标签字符串为数组
      this.articleForm.tags = this.articleForm.tagsStr.split(',').map(tag => tag.trim());
      // 发送PUT请求更新文章
      try {
        const url = `http://localhost:5000/api/articles/${this.articleForm.id}`;
        const response = await fetch(url, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.articleForm)
        });
        
        if (!response.ok) {
          throw new Error('Failed to update article');
        }
        
        // 重置表单
        this.showArticleEditor = false;
      } catch (error) {
        console.error('Error updating article:', error);
        alert('更新文章失败，请稍后重试');
      }
    }
  }
}
</script>

<style scoped>
/* 编辑器样式已集成在组件中 */

/* 代码块样式优化 */
:deep(pre) {
  background-color: #282c34 !important;
  color: #abb2bf;
  padding: 16px;
  border-radius: 6px;
  overflow-x: auto;
  margin: 16px 0;
  font-family: 'Fira Code', 'Courier New', monospace;
  font-size: 14px;
  line-height: 1.5;
  position: relative;
}

/* 复制按钮样式 */
:deep(.copy-button) {
  position: absolute;
  top: 8px;
  right: 8px;
  background-color: rgba(255, 255, 255, 0.1);
  color: #abb2bf;
  border: none;
  border-radius: 4px;
  padding: 6px 8px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  z-index: 10;
}

:deep(.copy-button:hover) {
  background-color: rgba(255, 255, 255, 0.2);
  color: #ffffff;
}

/* 复制通知样式 */
.code-copy-notification {
  position: fixed;
  top: 20px;
  right: 20px;
  background-color: #4caf50;
  color: white;
  padding: 10px 15px;
  border-radius: 4px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  z-index: 1000;
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.code-copy-notification.fade-out {
  opacity: 0;
  transform: translateY(-10px);
}

:deep(pre code) {
  background-color: transparent !important;
  padding: 0 !important;
  color: inherit;
  font-family: inherit;
  font-size: inherit;
  line-height: inherit;
  white-space: pre;
  word-wrap: normal;
}

/* 滚动条样式优化 */
:deep(pre::-webkit-scrollbar) {
  height: 8px;
}

:deep(pre::-webkit-scrollbar-track) {
  background: #1e1e1e;
  border-radius: 4px;
}

:deep(pre::-webkit-scrollbar-thumb) {
  background: #525252;
  border-radius: 4px;
}

:deep(pre::-webkit-scrollbar-thumb:hover) {
  background: #6e6e6e;
}
</style>