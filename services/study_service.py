#导入数据库连接函数
from db import get_connection

# wrong_count = cur.fetchone()["count"]
# 获取最新的五道错题和答案
def get_recent_wrong_answers(limit: int =5):
    #1:创建数据库对象
    conn=get_connection()

    #2:创建游标
    cur=conn.cursor()

    #3:执行数据命令
    # ORDER BY = 按照……排序
    # created_at = 按创建时间
    # DESC = 降序

    #LIMIT ? 限制最多返回多少条记录。

    #(limit,) 表示“只有一个元素的元组”
    cur.execute
    (
        """
            SELECT id, grammar_point, question, user_answer, correct_answer, created_at
            FROM wrong_answers
            ORDER BY created_at DESC
            LIMIT ? 
        """,(limit,)
    )

    #cur.fetchall(): 把刚才 SQL 查询到的所有结果都取出来。
    #dict(row): 把每一行转换成字典。

    rows =[
        dict(row)for row in cur.fetchall()
        ]
    conn.close()
    return rows

#获取薄弱的语法点
def get_weak_grammar_points():
    conn=get_connection()
    cur=conn.cursor()

    #COUNT(*) 表示“统计数量”。
    # AS wrong_count 表示给这个统计结果起个别名，叫：wrong_count
    
    #GROUP BY grammar_point :按照 grammar_point 分组
    cur.execute(
        """
        SELECT grammar_point, COUNT(*) AS wrong_count
        FROM wrong_answers
        GROUP BY grammar_point
        ORDER BY wrong_count DESC
        LIMIT 3
        """
    )
    rows=[dict(row) for row in cur.fetchall()]
    conn.close()
    return rows
