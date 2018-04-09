import os
import bin.my_lib.data_sqlite as data_sqlite
from PyQt5.QtWidgets import *
from urllib.request import urlopen
import bin.settings
import bin.my_lib.json_read_write as json_read_write

config = bin.settings.load_config()
RECEIVED_PATH = os.path.join(config["workplace"], "received")
WHERE = "receiver3.py"


def get_tasks():
    # 获取任务列表
    path_url = "%s/get_tasks/?tel=%s&status_code=10" % (config["site"], config["shop_tel"])
    result = urlopen(path_url)
    result_str = str(result.read())
    task_path = result_str[2:-1].split("*")
    if task_path == [""]:
        print(WHERE, "没有获取到新任务", task_path)
        return False
    for i in task_path:
        print(WHERE, "获取到新任务", i)
        segment = i.split("/")
        task_ID, tel, name, nick_name, address = segment[-2], segment[-3], None, None, None
        local_path, status_code, info, color, side = os.path.join(RECEIVED_PATH, tel, task_ID), "server_received", i, "0", "1"
        #data_sqlite.execute("INSERT INTO task (task_ID, tel, name, nick_name, address, local_path, status_code, info, color, side) "
         #                   "VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % ())
        if data_sqlite.insert_task(task_ID=task_ID, tel=tel, name=name, nick_name=nick_name, address=address,
                                   local_path=local_path, status_code=status_code, info=info, color=color, side=side):
            print(WHERE, "向本地数据库插入任务成功")
        else:
            print(WHERE, "向本地数据库插入任务失败")


def file_url(tel, task_ID):
    url = config["site"] + "/download/?path=/home/cloud_printing/received_files/%s/%s" % (tel, task_ID)
    return url


def get_files():
    tasks = data_sqlite.task_list("SELECT info FROM task "
                                  "WHERE status_code='server_received' or status_code='receiving'")
    # 状态为receiving的是上次下载出错遗留的任务
    if tasks == []:
        print(WHERE, "没有等待下载的任务", tasks)
    else:
        print(WHERE, "等待下载的任务", tasks)
        for info in tasks:
            info = info[0]
            fragment = info.split("/")
            tel = fragment[-3]
            task_ID = fragment[-2]
            files = fragment[-1].split(",")
            task_path = os.path.join(RECEIVED_PATH, tel, task_ID)
            # 任务号，json文件路径，状态码,返回的info信息
            try:
                # data_sqlite.execute("INSERT INTO task VALUES('%s','%s','receiving','%s')" % (task_ID, task_path, info))
                # cursor.execute("INSERT INTO task VALUES('task_test','path_test','code_test')")
                data_sqlite.execute("UPDATE task SET status_code='receiving' WHERE task_ID='%s'" % task_ID)
            except:
                # print("insert task ERROR or the task have exist")
                print(WHERE, "修改任务状态为receiving失败")
            # os.makedirs(task_path, 0o777, True)
            try:
                os.makedirs(task_path)
            except:
                print(WHERE, "文件夹已存在")
            for file in files:
                url = file_url(tel, task_ID) + "/" + file
                print(WHERE, url)
                try:
                    with open(os.path.join(task_path, file), "wb") as f:
                        try:
                            file_stream = urlopen(url)
                        except:
                            print(WHERE, "从服务器下载文件失败")
                            return False
                        f.write(file_stream.read())
                except:
                    print(WHERE, "保存文件失败")
                    return False
            '''
            # 修改info.json任务状态
            info_path = os.path.join(task_path, "info.json")
            info = json_read_write.read(info_path)
            if info:
                print(WHERE, "修改info状态成功", info)
                info["user"]["status"] = "received"
                if not json_read_write.write(info_path, info):
                    print(WHERE, "修改info.json任务状态失败")
                    return False
                    '''
            # 读取info.json
            info = json_read_write.read(os.path.join(RECEIVED_PATH, tel, task_ID, "info.json"))
            if info:
                print(WHERE, "DEBUG")
                user, name, nick_name, address = '', '', '', ''
                try:
                    user = info['user']
                    name = user['user_name']
                    nick_name = user['nick_name']
                    # nick_name = ''  # 等待服务端info.json文件修改
                    address = user['address']
                    # address = ''
                except:
                    print(WHERE, "info.json文件内容不匹配")
            else:
                print(WHERE, "读取info.json文件失败")
                return False
            # 修改数据库
            if data_sqlite.execute("UPDATE task SET "
                                   "status_code='received',"
                                   "name='%s',"
                                   "nick_name='%s',"
                                   "address='%s'"
                                   " WHERE task_ID='%s'"
                                           % (name, nick_name, address, task_ID)):
                print(WHERE, "修改任务的状态为received成功")
            else:
                print(WHERE, "修改任务的状态为received失败")
                return False


def start():
    # 向服务器请求一次任务并下载
    try:
        get_tasks()
        print(WHERE, "获取任务成功")
    except:
        print(WHERE, "获取任务失败")
    try:
        get_files()
        print(WHERE, "下载任务成功")
    except:
        print(WHERE, "下载任务失败")


# start()

