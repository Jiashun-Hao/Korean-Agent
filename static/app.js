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
        //向后端发送请求

        //await fetch:等待fetch（是浏览器里用来发送网络请求的函数）拿到结果以后再执行
        //请求地址为/api/chat
        const res= await fetch("/api/chat",{

            method:"POST", //POST：提交数据，GET获取数据
            headers:{
                "Content-Type":"application/json" //发送的数据的是JSON格式
            },
            body: JSON.stringify({message}) //JSON.stringify：变成json的字符串
        });

        //获取响应的数据，把格式变为json
        const data =await res.json();

        if (!res.ok){ //res.ok是一个布尔值 成功：200，失败 400 、 500
            throw new Error(data.error || "请求失败");
        }

        //显示返回结果到页面
        replyEl.textContent= data.reply || "" //|| or
        toolsEL.textContent= (data.tool_logs || []).join("\n"); //data.tool_logs有内容就用这个，没有就用空数组
        //join("\n") 多字符连接加换行
        
        
        //处理quiz题目数据
        //把返回的题目数组处理为合适的文字
        const quizeText=(data.quiz || []).map(
            (item,index)=>{
                return '${index+1}. ${item.question}\n答案：${item.answer}\n说明：${item.explanation}';
            }
        ).join("\n\n");
        quizEl.textContent=quizeText || "没有生成题目";
    } catch (error) {
        replyEl.textContent ='出错了：${err.message}';
    }

});