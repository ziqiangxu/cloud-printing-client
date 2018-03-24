import sqlite3
import bin.settings as settings
import os


def task_list(sql='SELECT * FROM task'):
    # 返回sql语句执行结果,元组列表
    try:
        data_connect = sqlite3.connect(os.path.join(settings.WORKPLACE, "received", "data.sqlite3"))
        # print("DEBUG", os.path.join(settings.WORKPLACE, "received", "data.sqlite3"))
        cursor = data_connect.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        data_connect.close()
    except:
        return False
    return result


def execute(sql):
    # 执行一句sql语句
    try:
        data_connect = sqlite3.connect(os.path.join(settings.WORKPLACE, "received", "data.sqlite3"))
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
