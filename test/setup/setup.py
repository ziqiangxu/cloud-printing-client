#安装程序
#创建必要的工作目录和复制执行代码
import os
import shutil
import win32api
try:
    os.mkdir("c://printer")
except WindowsError:
    win32api.MessageBox(None, "请手动删除C盘根目录的printer文件夹，注意备份其中的重要文件。并重新启动本安装程序")
os.mkdir("c:/printer/printed")
os.mkdir("c:/printer/local_task")
os.mkdir("c:/printer/received")
os.mkdir("c:/printer/bin")
os.system("copy ..\\bin C:\\printer\\bin")
shutil.copy("config.json","c:/printer/")
