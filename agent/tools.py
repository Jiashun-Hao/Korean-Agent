#列表，说明TOOLS是什么
TOOLS = [
    {
        "type": "function",
        "name": "get_recent_wrong_answers",
        "description": "최근 사용자의 오답 기록을 조회한다.",
        "parameters": {
            "type": "object",
            "properties": {
                "limit": {
                    "type": "integer",
                    "description": "가져올 오답 개수"
                }
            },
            "required": []
        }
    },
    {
        "type": "function",
        "name": "get_weak_grammar_points",
        "description": "사용자가 자주 틀리는 문법 포인트를 조회한다.",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "type": "function",
        "name": "generate_quiz",
        "description": "특정 문법 주제로 연습문제를 생성한다.",
        "parameters": {
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": "문법 포인트 이름"
                },
                "count": {
                    "type": "integer",
                    "description": "문제 개수"
                }
            },
            "required": ["topic"]
        }
    }
]