#用于练习的假数据
def generate_quiz(topic: str, count: int =3):
    quizzes = []
    for i in range(count):
        quizzes.append({
            "topic": topic,
            "question": f"[{topic}] 연습문제 {i+1}: 빈칸을 채워 보세요.",
            "answer": f"{topic} 관련 정답 예시",
            "explanation": f"{topic} 문법을 복습하기 위한 예시 문제입니다."
        })

    return quizzes    