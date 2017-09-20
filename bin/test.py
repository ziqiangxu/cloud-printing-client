import os
import json
"""
HOME_PATH = 'C:\\printer\\received'
user = os.path.join(HOME_PATH, "18796282979")
tasks = os.listdir(user)
for task in tasks:
    task_path = os.path.join(user, task)
    file_list = os.listdir(task_path)
    print(file_list)
    print(task_path)
    f = open(os.path.join(task_path, "info.json"), "r")
    info = json.load(f)
    print(info)
    for file in file_list:
        print(file)
"""
from ftplib import FTP
import os
import time
HOME_PATH = '/home/cloud_printing/received_files/'
LOCAL_PATH = 'C:\\printer\\received'
ERROR_TIMES = 0
ftp = FTP()
timeout = 120
port = 21
ip = "45.76.222.90"
print("test:开始连接ftp站点")
try :
    ftp.connect(ip, port=21, timeout=120)
except TimeoutError:
    print("test:连接ftp超时")
ftp.login('vsftp', 'abc123cloud')


def download(id, task):
    url = HOME_PATH + id + "/" + task + "/"
    print("test:", url)
    print("test:", ftp.nlst(url))
download("18796282979", "22759321")
