from templates.config import conn

cur = conn.cursor()

def add_user(username, password, id ,r_date):
    # sql commands
    sql = "INSERT INTO user(Id,Name,Password,Registration_date) VALUES ('%s','%s','%s','%s')" %(id, username, password, r_date)
    # execute(sql)
    cur.execute(sql)
    # commit
    conn.commit()  # 对数据库内容有改变，需要commit()
    conn.close()

