from ftplib import FTP
import os
import time
import bin.json_read_write as json_wr
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


def download(user_id, task_id):
    task_url = HOME_PATH + user_id + "/" + task_id + "/"
    task_path_local = os.path.join(HOME_PATH_LOCAL, user_id, task_id)
    os.makedirs(task_path_local, 0o777, True)
    print(WHERE ,"获取用户%s的%s任务文件" % (user_id, task_id), task_url)
    try:
        file_list = ftp.nlst(task_url)
    except:
        print(WHERE, "获取用户%s的%s任务文件列表失败" % (user_id, task_id))
        return False
    for file in file_list:
        name = file.split("/").pop()
        f = open(os.path.join(task_path_local, name), "wb")
        print(WHERE, "获取文件%s" % file)
        ftp.retrbinary("RETR " + file, f.write)
        f.close()
        info_path = os.path.join(task_path_local, "info.json")
    info = json_wr.read(info_path)
    info["user"]["status"] = "received"
    json_wr.write(info_path, info)
    return True


def start():
    connect()
    while True:
        # 测试区域
        user_id2 = "18796282979"
        try:
            task_list = ftp.nlst(HOME_PATH + user_id2 + "/")
            print(WHERE, "获取任务号列表成功", task_list)
        except:
            print(WHERE, "获取任务号列表失败")
        # 测试区域
        for task_id2 in task_list:
            task_id2 = task_id2.split("/").pop()
            task_path_local = os.path.join(HOME_PATH_LOCAL, user_id2, task_id2)
            try:
                file_list_local = os.listdir(task_path_local)
            except:
                file_list_local = []
            if "info.json" in file_list_local:
                info = json_wr.read(os.path.join(task_path_local, "info.json"))
                if not info:
                    download(user_id2, task_id2)
            else:
                download(user_id2, task_id2)
        time.sleep(5)
        print(WHERE, "download程序循环运行")

