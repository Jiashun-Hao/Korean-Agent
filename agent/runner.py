#Agent调度器代码
from services.study_service import get_recent_wrong_answers,get_weak_grammar_points
from services.quiz_service import generate_quiz

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