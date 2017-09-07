#!coding=utf-8
# 从中转文件服务器获取用户文件，存放在本地的received文件夹中
from ftplib import FTP
import os
HOME_PATH = '/home/cloud_printing/received_files'
ftp = FTP()
timeout = 120
port = 21
try:
    ftp.connect('45.76.222.90', port=21, timeout=120)
    ftp.login('vsftp', 'abc123cloud')
except:
    print("FTP登录------失败")


def get_user():
    user_error = 0
    while True:
        if user_error:
            print("获取用户列表------重试%d次"%user_error)
        try:
            ftp.cwd(HOME_PATH)
            user_list = ftp.nlst()
            print(user_list)
            return user_list
        except:
            user_error += 1


def get_task(user):
    user_path = os.path.join(HOME_PATH, user)
    task_error = 0
    while True:
        if task_error:
            print("获取%s的任务列表------重试%d次" % (user, task_error))
        try:
            ftp.cwd(user_path)
            tasks = ftp.nlst()
            return tasks
        except:
            task_error += 1


def get_file(user, task):
    file_error = 0
    while True:
        if file_error:
            print("获取%s的%s任务文件------重试%d次"% (user, task, file_error))
        try:
            ftp.cwd(os.path.join(HOME_PATH, user, task))
            files = ftp.nlst()
            return files
        except:
            file_error += 1


def download_file(user, task, user_task_files):
    if "info.json" in user_task_files:
        local_path = os.path.join("/printer/received/", user, task)
        try:
            os.makedirs(local_path, 0o777, True)
        except:
            print("创建任务目录失败")
        print("%s的%s任务文件上传完毕，可以下载" % (user, task))

        for file in user_task_files:
            file_path = os.path.join(HOME_PATH, user, task, file)
            print(file_path)
            try:
                f = open(os.path.join(local_path, file), 'wb')
            except:
                print("保存%s出错"%(os.path.join(local_path, file)))
            while True:
                try:
                    ftp.retrbinary("RETR " + file_path, f.write)
                    break
                except:
                    print("重新下载%s" %file_path)
    else:
        print("%s的%s任务文件部分上传，暂不下载" % (user, task))
# '''
user_list = get_user()
for user in user_list:
    task_list = get_task(user)
    for task in task_list:
        file_list = get_file(user, task)
        print("正在处理：", os.path.join(HOME_PATH, user, task))
        download_file(user, task, file_list)

ftp.quit()