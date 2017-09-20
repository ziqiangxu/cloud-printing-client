from ftplib import FTP
import os
import time
import json_read_write
HOME_PATH = '/home/cloud_printing/received_files/'
HOME_PATH_LOCAL = 'C:\\printer\\received'
WHERE = "receiver:"
ftp = FTP()


def connect():
    try:
        timeout = 120
        port = 21
        ip = "45.76.222.90"
        try:
            print(WHERE, ":连接ftp站点：%s" % ip)
            ftp.connect(ip, port=21, timeout=120)
            print(WHERE, "连接成功")
        except TimeoutError:
            print(WHERE, "连接ftp超时")
        try:
            ftp.login('vsftp', 'abc123cloud')
            print(WHERE, "登录成功")
        except:
            print(WHERE, "登录失败")
        return True
    except:
        return False


def download(user_id, task):
    task_url = HOME_PATH + user_id + "/" + task + "/"
    task_path_local = os.path.join(HOME_PATH_LOCAL, user_id, task)
    os.makedirs(task_path_local, 0o777, True)
    print(WHERE ,"获取用户%s的%s任务文件" % (user_id, task), task_url)
    try:
        file_list = ftp.nlst(task_url)
    except:
        print(WHERE, "获取用户%s的%s任务文件列表失败" % (user_id, task))
        return False
    for file in file_list:
        name = file.split("/").pop()
        f = open(os.path.join(task_path_local, name), "wb")
        print(WHERE, "获取文件%s" % file)
        ftp.retrbinary("RETR " + file, f.write)
        f.close()

    info_local = os.path.join(task_path_local, "info.json")
    info = {}
    info = json_read_write.read(info_local)
    if not info:
        return False
    info["user"]["status"] = "received"
    if not json_read_write.write(info_local, info):
        return False
    return True

def start():
    connect()
    while True:
        # 测试区域
        user_id2 = "18796282979"
        task_list_local = ""
        file_list_local = []
        try:
            task_list = ftp.nlst(HOME_PATH + user_id2 + "/")
            print(WHERE, "获取任务号列表成功", task_list)
        except:
            print(WHERE, "获取任务号列表失败")
        # 测试区域
        for task2 in task_list:
            task2 = task2.split("/").pop()
            try:
                file_list_local = os.listdir(os.path.join(HOME_PATH_LOCAL, user_id2, task2))
            except:
                print(WHERE, "本地没有用户%s的%s任务" % (user_id2, task2))
                if not download(user_id2, task2):
                    print(WHERE, "任务下载失败")
            '''
            if "info.json" in file_list:
                print(WHERE, "用户%s的%s任务已下载" % (user_id2, task2))
            else:
                print("开始下载", user_id2, task2)
                download(user_id2, task2)
                '''
        time.sleep(5)
        print(WHERE, "download程序循环运行")

