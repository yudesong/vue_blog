import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 导入Flask应用
from app import app

if __name__ == '__main__':
    # 从环境变量获取配置，或者使用默认值
    debug = os.environ.get('FLASK_DEBUG', '1') == '1'
    host = os.environ.get('FLASK_RUN_HOST', '127.0.0.1')
    port = int(os.environ.get('FLASK_RUN_PORT', '5000'))
    
    # 运行Flask应用
    app.run(debug=debug, host=host, port=port)