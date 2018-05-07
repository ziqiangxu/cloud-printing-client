import sqlite3
import os
print(__file__, os.getcwd())
CONFIG = {"workplace": "c:/printer"}  # 根据当前路径找到data.sqlite


def task_list(sql='SELECT * FROM task'):
    # 返回sql语句执行结果,元组列表
    try:
        db_path = os.path.join(CONFIG["workplace"], "received", "data.sqlite3")
        print(__file__, "数据库文件路径", db_path)
        data_connect = sqlite3.connect(db_path)
        # print("DEBUG", os.path.join(settings.WORKPLACE, "received", "data.sqlite3"))
        cursor = data_connect.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        data_connect.close()
    except:
        print(__file__, sql, "执行失败")
        return False
    return result


def execute(sql):
    # 执行一句sql语句
    print(__file__, "execute the sql:", sql)
    try:
        data_connect = sqlite3.connect(os.path.join(CONFIG["workplace"], "received", "data.sqlite3"))
        cursor = data_connect.cursor()
        cursor.execute(sql)
        data_connect.commit()
        res = cursor.fetchall()
    except:
        return False
    data_connect.close()
    if res:
        return res
    else:
        return True


def insert_task(task_ID, tel, name, nick_name, address, local_path, status_code, info, color, side):
    try:
        execute(
            "INSERT INTO task (task_ID, tel, name, nick_name, address, local_path, status_code, info, color, side) "
            "VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"
            % (task_ID, tel, name, nick_name, address, local_path, status_code, info, color, side)
            )
        return True
    except:
        return False

# print(task_list('SELECT task_ID,local_path FROM task'))
