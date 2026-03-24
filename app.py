#Flask 后端入口文件。
#启动网页服务，把前端接收来的聊天消息，把消息交给run_local_agent()处理，然后结果发会给前端
import os

#读取 .env 文件里的配置，并加载成环境变量
from dotenv import load_dotenv
# Flask
# 用来创建 Flask 应用对象。

# jsonify
# 把 Python 数据转换成 JSON 响应返回给前端。

# render_template
# 用来返回 HTML 页面。

# request
# 用来读取前端发过来的请求数据
from flask import Flask, jsonify, render_template,request

from services.db import init_db, seed_demo_data
from agent.runner import run_local_agent

#加载.env的配置文件
load_dotenv()


def create_app():
    #创建一个 Flask 应用实例，
    #路由、配置、启动，都是围绕它来的。
    app = Flask(__name__)

    #给Flask的对象配置一个SECRET_KEY
    app.config["SECRET_KEY"]=os.getenv("SECRET_KEY","dev-secret-key")
    #os.getenv("SECRET_KEY", "dev-secret-key")
    # 意思是：
    # 先去环境变量里找 SECRET_KEY
    # 如果找不到，就用默认值 "dev-secret-key"

    #定义首页路由
    @app.route("/")
    def index():
        return render_template("index.html")
    

    #定义聊天接口
    #当前端向/api/chat这个地址发送POST请求的时候，执行下面的函数
    @app.route("/api/chat",methods=["POST"])
    def chat():
        app=Flask(__name__)
        data =request.get_json(silent=True) or {} #解析失败，返回None
        
        # 取出用户信息
        message=(data.get("message")or "").strip() #.strip()去除首尾空格和换行符
        if not message:
            return jsonify({"error":"message is required"}), 400
        
        
        #调用本地的Agent
        #把用户输入的 message 交给 run_local_agent() 处理。
        result = run_local_agent(message)

        #把 Python 字典 result 转成 JSON 响应发回给前端。
        return jsonify(result)
    
    return app

app = create_app()

if __name__ =="__main__":
    init_db()
    seed_demo_data()
    app.run(debug=True)