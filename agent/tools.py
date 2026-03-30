TOOLS = [
    {
        "type": "function",
        "name": "get_recent_wrong_answers",
        "description": "获取用户最近的错题记录，用于分析最近的学习弱点。",
        "parameters": {
            "type": "object",
            "properties": {
                "limit": {
                    "type": "integer",
                    "description": "返回的错题数量，默认 5"
                }
            },
            "required": []
        }
    },
    {
        "type": "function",
        "name": "get_weak_grammar_points",
        "description": "统计用户最容易出错的语法点。",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "type": "function",
        "name": "generate_quiz",
        "description": "根据指定语法点生成练习题。",
        "parameters": {
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": "要练习的语法点名称"
                },
                "count": {
                    "type": "integer",
                    "description": "题目数量，默认 3"
                }
            },
            "required": ["topic"]
        }
    }
]