import sqlite3
import bin.settings
import os
WHERE = "my_lib/data_sqlite.py"
CONFIG = bin.settings.load_config()


def task_list(sql='SELECT * FROM task'):
    # 返回sql语句执行结果,元组列表
    try:
        db_path = os.path.join(CONFIG["workplace"], "received", "data.sqlite3")
        print(WHERE, "数据库文件路径", db_path)
        data_connect = sqlite3.connect(db_path)
        # print("DEBUG", os.path.join(settings.WORKPLACE, "received", "data.sqlite3"))
        cursor = data_connect.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        data_connect.close()
    except:
        print(WHERE, sql, "执行失败")
        return False
    return result


def execute(sql):
    # 执行一句sql语句
    try:
        data_connect = sqlite3.connect(os.path.join(CONFIG["workplace"], "received", "data.sqlite3"))
        cursor = data_connect.cursor()
        cursor.execute(sql)
        data_connect.commit()
    except:
        return False
    data_connect.close()
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
