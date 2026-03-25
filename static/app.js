// JS：轻量的无需保存到后端的逻辑处理

// 点击按钮
// 输入内容
// 下拉选择
// 拖拽
// 弹窗
// 切换页面状态

// 做一些轻量逻辑：
// 输入不能为空
// 手机号长度检查
// 页面实时预览
// 计算价格小计
// 把后端返回的数据渲染出来

//JSON ：就是一种专门用来保存和传输数据的文本格式。

//获取网页上的元素
//找HTML里面的id
const sendBtn = document.getElementById("sendBtn");
const messageEl = document.getElementById("message"); //输入框
const replyEl = document.getelementsById("reply");
const toolsEl = document.getelementsById("tools");
const quizEl=document.getelementsById("quiz");

//给按钮添加一个click以后的动作
//addEventListener元素监听器

// async () => { ... }
// 这是一个匿名箭头函数，意思是：“点击以后，要执行这一整段代码。”
sendBtn.addEventListener("click",async()=>{
    //messageEl.value.trim();输入框里面的值.属性.去除前后的空格
    const message =messageEl.value.trim();

    if (!message){
        alert("请输入内容")
        return;
    }

    //在收到数据前先更新一下页面
    //文字回复区域
    replyEl.textContent ="处理中...";
    //工具日志清空
    toolsEl.textContent="";
    //清空题目
    quizEl.textContent="";

    //处理请求，捕获异常
    try {
        
        
    } catch (error) {
        
    }

})