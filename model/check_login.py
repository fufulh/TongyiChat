from templates.config import conn
from datetime import datetime
cur = conn.cursor()


def is_null(username,password,id):
	if(username==''or password==''or id==''):
		return True
	else:
		return False


def is_existed(username,password):
	sql="SELECT * FROM user WHERE Name ='%s' and Password ='%s'" %(username,password)
	cur.execute(sql)
	result = cur.fetchall()
	if (len(result) == 0):
		return False
	else:
		return True

def exist_user(username):
	sql = "SELECT * FROM user WHERE Name ='%s'" % (username)
	cur.execute(sql)
	result = cur.fetchall()
	if (len(result) == 0):
		return False
	else:
		return True


def update_login_time(username, password):
	# 更新登录时间
	current_time = datetime.now()
	current_time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
	sql = "UPDATE user SET Last_login_time = %s WHERE Name = %s AND Password = %s"
	cur.execute(sql, (current_time_str, username, password))
	conn.commit()  # 提交事务

	return True, "登录时间更新成功"
