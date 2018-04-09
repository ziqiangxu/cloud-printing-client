import bin.my_lib.json_read_write as json_read_write
import platform
from PyQt5.QtWidgets import *

WHERE = "settings.py"
OS = platform.system()


def load_config():
    if OS == "Linux":
        print(WHERE, "当前运行的操作系统是Linux")
        config_path = "/home/xu/printer/config.json"

    elif OS == "Windows":
        print(WHERE, "当前运行的操作系统是Windows")
        config_path = "c:\\printer\\config.json"
    else:
        print(WHERE, "不支持的平台")
        return False
    config = json_read_write.read(config_path)
    if not config:
        print(WHERE, "未找到config.json文件")
    # 并对参数进行检查
    config["os"] = OS
    config["config_path"] = config_path
    return config
