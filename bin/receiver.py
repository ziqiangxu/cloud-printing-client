# coding=utf-8
# 从中转文件服务器获取用户文件，存放在本地的received文件夹中
from ftplib import FTP
import os
import time
HOME_PATH = '/home/cloud_printing/received_files'
LOCAL_PATH = 'C:\\printer\\received'
ERROR_TIMES = 0
ftp = FTP()
timeout = 120
port = 21


def get_user():
    print("receiver:", HOME_PATH)
    ERROR_TIMES = 0
    while True:
        if ERROR_TIMES:
            time.sleep(3)
            print("receiver:获取用户列表------重试%d次"%ERROR_TIMES)
        try:
            ftp.cwd(HOME_PATH)
            user_list = ftp.nlst()
            print(user_list)
            return user_list
        except:
            ERROR_TIMES += 1


def get_task(user):
    user_path = os.path.join(HOME_PATH, user).replace('\\', '/')
    print("receiver:", user_path)
    ERROR_TIMES = 0
    while True:
        if ERROR_TIMES:
            print("receiver:获取%s的任务列表------重试%d次" % (user, ERROR_TIMES))
        try:
            ftp.cwd(user_path)
            tasks = ftp.nlst()
            return tasks
        except:
            ERROR_TIMES += 1


def get_file(user, task):
    ERROR_TIMES = 0
    task_path = os.path.join(HOME_PATH, user, task).replace('\\', '/')
    print("receiver:", task_path)
    while True:
        if ERROR_TIMES:
            print("receiver:获取%s的%s任务文件------重试%d次"% (user, task, ERROR_TIMES))
        try:
            ftp.cwd(task_path)

            files = ftp.nlst()
            return files
        except:
            ERROR_TIMES += 1


def download_file(user, task, user_task_files):
    if "info.json" in user_task_files:
        user_task_files.remove("info.json")
        local_path = os.path.join("/printer/received/", user, task).replace('/', "\\")
        try:
            print("receiver:创建目录", local_path)
            os.makedirs(local_path, 0o777, True)
        except:
            print("receiver:创建任务目录失败")
        print("%s的%s任务文件上传完毕，可以下载" % (user, task))

        for file in user_task_files:
            file_path = os.path.join(HOME_PATH, user, task, file).replace('\\','/')
            try:
                f = open(os.path.join(local_path, file), 'wb')
            except:
                print("receiver:保存%s出错"%(os.path.join(local_path, file)))
            while True:
                try:
                    ftp.retrbinary("RETR " + file_path, f.write)
                    break
                except:
                    print("receiver:重新下载%s" %file_path)
        while True:
            try:
                f = open(os.path.join(local_path, "info.json"), "wb")
                try:
                    ftp.retrbinary("RETR info.json", f.write)
                    break
                except:
                    print("receiver:下载%s任务的info.json文件失败" % task)
                break
            except:
                os.remove(os.path.join(local_path, "info.json"))
                print("receiver:保存%s任务的info.json文件失败" % task)
    else:
        print("receiver:%s的%s任务文件部分上传，暂不下载" % (user, task))


def download():
    user_list = get_user()
    for user in user_list:
        task_list = get_task(user)
        print("receiver:", task_list)
        for task in task_list:
            os.makedirs(os.path.join(LOCAL_PATH, user, task), 0o777, True)
            is_download = "info.json" in os.listdir(os.path.join(LOCAL_PATH, user, task))
            if is_download:
                print("receiver:%s任务已包含info.json文件,表示已下载"% task)
            else:
                file_list = get_file(user, task)
                print("receiver:正在处理：", os.path.join(HOME_PATH, user, task))
                download_file(user, task, file_list)

    # ftp.quit()


def start():
    while True:
        print("正在连接")
        try:
            ftp.connect('45.76.222.90', port=21, timeout=120)
            ftp.login('vsftp', 'abc123cloud')
            break
        except:
            print("receiver:FTP登录------失败")
    while True:
        print("receiver:下载程序正在运行")
        download()
        time.sleep(5)


