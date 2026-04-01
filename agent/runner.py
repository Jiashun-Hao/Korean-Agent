#Agent调度器代码
#第一次，用户问题--GPT，GPT回复，我要调用工具A、B
#python 执行工具A、B
#第二次，python把工具结果发回给GPT，GPT生成最终回复
import json #处理JSON格式的数据
import os #导入OS模块

from openai import OpenAI

from agent.prompt import SYSTEM_PROMPT #导入系统提示词
from agent.tools import TOOLS #导入看模型可以调用哪些功能

#本地工具
from services.study_service import get_recent_wrong_answers,get_weak_grammar_points
from services.quiz_service import generate_quiz

#创建OpenAI客户端
client=OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def execute_tool(tool_name, arguments):
    if tool_name == "get_recent_wrong_answers": #如果是调用这个工具
        limit = arguments.get("limit",5) # 如果参数里面有limit就用，如果没有就用5
        return get_recent_wrong_answers(limit=limit)
    
    if tool_name == "get_weak_grammar_points":
        return get_weak_grammar_points()
    
    if tool_name == "generate_quiz":
        topic = arguments["topic"]
        count = arguments.get("count",3) #取count的参数，没有就取3
        return generate_quiz(topic=topic,count=count) #调用本地函数，生成测试题
    
    raise ValueError(f"Unkonwn tool: {tool_name}")

#定义一个函数，从OpenAI返回response对象里面提取文本的内容
def extract_text_from_response(response):
    final_text=""

    for item in response.output: #用item遍历response.output中的每一项
        if item.type =="message": #提取模型说的话
            for content in item.content:  #一个message里面可能有多个内容块，所以继续遍历
                if content.type == "output_text":#如果这个内容的类型是文本，就处理
                  final_text+=content.text

    return final_text.strip() #返回文本祛除首尾空格

#主函数
def run_openai_agent(user_message: str): #用户输入的消息会传入这里
    tool_logs =[] #日志

    #第一次请求OpenAI
    #判断模式是直接回答，还是决定调用工具
    response = client.responses.create(
        model="gpt-4.1",
        instructions=SYSTEM_PROMPT, #发送系统提示词给模型
        input=user_message, #把用户的输入发给模型
        tools=TOOLS #工具定义发给模型
    )

    function_calls=[] #如果模型决定调用工具，就把调用的工具信息记录
    for item in response.output:
        if item.type == "function_call":
            function_calls.append(item)

    if not function_calls: #如果工具记录是空的，那么就说明模型没有调用任何工具直接输出，或者发生错误没有内容
        return {
            "reply": extract_text_from_response(response) or "暂时没有内容。",
            "tool_logs":[],
            "quiz":[],
        }
    #else
    #如果模型调用了工具
    tool_outputs=[]

    for call in function_calls: #遍历函数和工具调用
        tool_name = call.name #取出调用的工具名
        argumnets = json.loads(call.arguments or "{}")

        #json.dumps:把python字典转化成json字符串
        tool_logs.append(f"{tool_name}({json.dumps(argumnets, ensure_ascii=False)})")#nsure_ascii=False 中文不转义
        
        #根据工具名取调用真实的本地函数
        result = execute_tool(tool_name,argumnets)

        #把执行结果整理成OpenAI能识别的格式，加入tool_outputs
        tool_outputs.append({
            "type":"function_call_output",
            "call_id":call.call_id, #分别输出结果为哪一次的函数调用
            "output":json.dumps(result,ensure_ascii=False)
        })

    second_resopnse=client.responses.create(
        model="gpt-4.1",
        instructions=SYSTEM_PROMPT,
        previous_response_id=response.id,
        input=tool_outputs
    )

    quiz=[]
    for output_item in tool_outputs:
       try:
            parsed = json.loads(output_item["output"])
            if(
                isinstance(parsed, list)
                and parsed
                and isinstance(parsed[0],dict)
                and "question" in parsed[0]
            ):
                quiz = parsed
       except Exception:
           pass     
    return {
            "reply":extract_text_from_response(second_resopnse) or "暂时没有内容",
            "tool_logs": tool_logs,
            "quiz":quiz,

    }      
def run_local_agent(user_message: str):
    weak_points=get_weak_grammar_points()
    recent_wrong=get_recent_wrong_answers(limit=3)

    if weak_points: #weak_points:不为空

        #取出 weak_points 列表里的第 1 个元素，也就是最弱的那个语法点，再取其中的 "grammar_point" 字段。
        main_topic = weak_points[0]["grammar_point"]
    else:
        main_topic ="-지만"   

    quiz=generate_quiz(main_topic, count=3)

    return {
            "reply": (
                f"根据你最近的学习记录，我觉得你现在最需要复习的是 {main_topic}。\n"
                f"我也参考了最近的错题，先给你安排 3 道相关练习。"
            ),
            "tool_logs": [
                "get_weak_grammar_points()",
                "get_recent_wrong_answers(limit=3)",
                f'generate_quiz(topic="{main_topic}", count=3)'
            ],
            "quiz": quiz,
            "recent_wrong": recent_wrong,
        }