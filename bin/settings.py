import platform
import bin.my_lib.data_sqlite as db
import os

OS = platform.system()
PRINTER_LIST = []


def load_config():
    print(__file__, "当前操作系统--", OS)
    if OS == "Linux":
        home = os.environ['HOME']
        config_path = os.path.join(home, 'printer/config.json')

    elif OS == "Windows":
        config_path = "c:/printer/config.json"
        import win32print
        for printer in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL):
            PRINTER_LIST.append(printer[2])
    else:
        print(__file__, "不支持的平台")
        return False
    # config 是一个字典
    config = {}
    res = db.execute('SELECT * FROM KEY_VALUE')
    if not res:
        return False
    for i in res:
        config[i[0]] = i[1]
    # 并对参数进行检查
    config["os"] = OS
    config["config_path"] = config_path
    return config
