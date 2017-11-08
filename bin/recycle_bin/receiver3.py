import os
import sqlite3
import win32api
from urllib.request import urlopen

import bin.lib.json_read_write as json_read_write

config = json_read_write.read("c:\\printer\\config.json")
SITE = config["site"]
LOCAL_PATH = "\\printer\\received"
WHERE = "receiver3"
shop_tel = config["shop_tel"]
print(shop_tel)
task_connection = sqlite3.connect(os.path.join(LOCAL_PATH, "task.sqlite3"))
cursor = task_connection.cursor()
if not shop_tel:
    win32api.MessageBox(None, "请在C:\\printer\config.json文件填入您的账号和密码!")


def get_tasks():
    path_url = "%s/get_tasks/?tel=%s&status_code=10" % (SITE, shop_tel)
    result = urlopen(path_url)
    result_str = str(result.read())
    task_path = result_str[2:-1].split("*")
    print(WHERE, task_path)
    return task_path


def file_url(tel, task_ID):
    url = SITE + "/download/?path=/home/cloud_printing/received_files/%s/%s" % (tel, task_ID)
    return url


def get_files():
    tasks = get_tasks()
    if not tasks[0] == "":
        for info in tasks:
            fragment = info.split("/")
            tel = fragment[-3]
            task_ID = fragment[-2]
            files = fragment[-1].split(",")
            task_path = os.path.join(LOCAL_PATH, tel, task_ID)
            # 任务号，json文件路径，状态码,返回的info信息
            try:
                cursor.execute("INSERT INTO task VALUES('%s','%s','receiving','%s')" % (task_ID, task_path, info))
                # cursor.execute("INSERT INTO task VALUES('task_test','path_test','code_test')")
            except:
                print("insert task ERROR or the task have exist")
            # os.makedirs(task_path, 0o777, True)
            try:
                os.makedirs(task_path)
            except:
                print(WHERE, "file has exist,create file failed,execute next")
            for file in files:
                url = file_url(tel, task_ID) + "/" + file
                print(url)
                try:
                    with open(os.path.join(task_path, file), "wb") as f:
                        try:
                            file_stream = urlopen(url)
                        except:
                            print(WHERE, "get files from the server failed")
                            return False
                        f.write(file_stream.read())
                except:
                    print(WHERE, "save files failed")
                    return False
            # 修改info.json任务状态
            info_path = os.path.join(task_path, "info.json")
            info = json_read_write.read(info_path)
            if info:
                print(WHERE, "修改info状态成功", info)
                info["user"]["status"] = "received"
                if not json_read_write.write(info_path, info):
                    print(WHERE, "修改info.json任务状态失败")
                    return False
            # 修改数据库
            try:
                cursor.execute("UPDATE task SET status_code='received' WHERE task_ID='%s'" % task_ID)
                print("received the files")
            except:
                print("update task error")
                return False
    else:
        print(WHERE, "没有收到任务", tasks)


def start():
    try:
        get_files()
    except:
        print(WHERE, "下载任务失败")
        return False
    # 执行完毕提交数据库修改
    task_connection.commit()
    print("commit the sqlite3")
    task_connection.close()


start()

