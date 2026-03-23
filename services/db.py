import os
import sqlite3

BASE_DIR = os.path.dirname( #BASE_DIR 现在是根目录文件夹的名字
    os.path.dirname(
        os.path.abspath(__file__) #__file__：当前文件
    )

)

#INSTANCE 路径
INSTANCE_DIR=os.path.join(BASE_DIR,"instance") 

#数据库文件路径
DB_PATH =os.path.join(INSTANCE_DIR,"app.db")

#数据库连接函数，返回一个数据库对象
def get_connection():

    os.makedirs(INSTANCE_DIR,exist_ok=True)
    conn=sqlite3.connect(DB_PATH) #conn为数据库对象
    conn.row_factory=sqlite3.Row #conn.row_factory为对象的返回格式，调用sqlite3.Row的格式返回，可以进行字典查询

    return conn

#建立数据表
# -- grammar_points：语法点
# -- wrong_answers：错题
# -- study_logs：学习日志

def init_db():
    conn= get_connection()
    #游标：游标是用来执行数据库操作命令，并保存这次操作状态的对象。
    cur=conn.cursor()

    # 编号 id
    # 名称 name
    # 说明 description
    # 难度 level
    # 例句 example

    #grammar_points 表
    cur.execute( #创建表
     # CREATE TABLE   创建表
     # AUTOINCREMENT    自动递增   
    """
    CREATE TABLE IF NOT EXISTS grammar_points(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        level TEXT,
        example TEXT
    )
    """
    )

    #wrong_answers： 表
    cur.execute(
    #TIMESTAMP 时间类型
    #DEFAULT CURRENT_TIMESTAMP 如果你插入数据时没有手动写这个时间，就自动使用“当前时间”
    """
    CREATE TABLE IF NOT EXISTS wrong_answers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        grammar_point TEXT NOT NULL,
        question TEXT NOT NULL,
        user_answer TEXT,
        correct_answer TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
        
    """
    )

    #study_logs：学习日志表
    cur.execute("""
    CREATE TABLE IF NOT EXISTS study_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        study_date TEXT NOT NULL,
        summary TEXT,
        duration_minutes INTEGER DEFAULT 0
    )
    """)

    conn.commit() #保存
    conn.close() #关闭连接

#测试函数，预先加一些东西到数据库
def seed_demo_data():
    conn=get_connection()
    cur=conn.cursor()

    cur.execute(
        #查看表里面一共有多少条记录
        """
        SELECT COUNT(*) AS count FROM grammar_points
        """
    )

    #cur.fetchone() 从当前查询结果里取出一行

    count =cur.fetchone()["count"]
    #多命令连贯写法，等价于
    #row = cur.fetchone()
    #value = row["count"]

    if count == 0:
        demo_rows = [
            ("-지만", "表示转折：虽然……但是……", "TOPIK 2", "비가 오지만 학교에 갔어요."),
            ("-는 것", "动词名词化", "TOPIK 2", "책을 읽는 것이 재미있어요."),
            ("-(으)ㄴ 줄 알았어요", "原以为……", "TOPIK 3", "벌써 끝난 줄 알았어요."),
        ]
        ## ecutemany：把demo_rows里面的数据行轮流执行
        cur.executemany("""
            INSERT INTO grammar_points (name, description, level, example)
            VALUES (?, ?, ?, ?)
            """, 
            demo_rows
            )
    cur.execute("SELECT COUNT(*) AS count FROM wrong_answers")
    wrong_count = cur.fetchone()["count"]
    if wrong_count == 0:
        demo_wrong = [
        ("-지만", "다음 문장을 완성하세요: 비가 오___ 학교에 갔어요.", "비가 오면", "비가 오지만"),
        ("-는 것", "한국어를 공부하___ 재미있어요.", "공부하는", "공부하는 것"),
        ]

        cur.executemany("""
        INSERT INTO wrong_answers (grammar_point, question, user_answer, correct_answer)
        VALUES (?, ?, ?, ?)
        """, demo_wrong)

    conn.commit()
    conn.close()


# def test_read():
#     conn = get_connection()
#     cur = conn.cursor()

#     cur.execute("SELECT * FROM grammar_points")
#     rows = cur.fetchall()

#     print("grammar_points 表里的数据：")
#     for row in rows:
#         print(dict(row))

#     cur.execute("SELECT * FROM wrong_answers")
#     rows = cur.fetchall()

#     print("wrong_answers 表里的数据：")
#     for row in rows:
#         print(dict(row))

#     conn.close()

# if __name__ == "__main__":
#     init_db()
#     seed_demo_data()
#     test_read()
#     print("测试完成。")