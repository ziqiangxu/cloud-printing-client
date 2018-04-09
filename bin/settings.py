import bin.my_lib.json_read_write as json_read_write
import platform
from PyQt5.QtWidgets import *

WHERE = "settings.py"
OS = platform.system()
if OS == "Linux":
    print(WHERE, "当前运行的操作系统是Linux")
    config = json_read_write.read("/home/xu/printer/config.json")

elif OS == "Windows":
    print(WHERE, "当前运行的操作系统是Windows")
    config = json_read_write.read("c:\\printer\\config.json")

else:
    print(WHERE, "不支持的平台")
if not config:
    print(WHERE, "未找到config.json文件")

SITE = config["site"]
SHOP_TEL = config["shop_tel"]
WORKPLACE = config["workplace"]
PROJECT_NAME = "cloud_printing_client"
AUTO_DOWNLOAD_TASKS = config["auto_download_tasks"]