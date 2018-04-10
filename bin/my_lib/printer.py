# coding=utf-8
# 打印的核心程序
# 只需要传入文件夹路径就可以根据文件夹下info.json提供的要求进行打印。
# 客户端计算机必须满足两个要求：
# 1.设置pdf的默认打印程序（本程序虽然可以处理其它类型的文件，但是排版可能不容乐观）
# 2.选择了默认打印机，不能是pdf打印机（因为pdf打印机工作时需要一个保存文件路径）
# 3.使用sumatrapdf程序进行打印机控制


import os
import json
import time
import win32print
import win32api
import re
WHERE = "lib/printer.py"


def task():    # 获取默认打印机的工作状态
    printer_name = win32print.GetDefaultPrinter()
    handle_printer = win32print.OpenPrinter(printer_name)    # 获取打印机句柄
    printer_info = win32print.GetPrinter(handle_printer, 2)    # 调用相关函数进行信息查询
    task_list = win32print.EnumJobs(handle_printer,0,10)    # 参数（句柄，编文档号，枚举条数）
    return printer_info["cJobs"]    # 获取当前打印机任务数目


def __doc__():
    return "receiver:这是打印文档的核心函数，需要传入打印文件夹的路径作为参数"


def print_files(task_path):
    # 本函数将根据info.json要求打印目标文件夹的所有文件【绝对路径】
    get_info = open(os.path.join(task_path, "info.json"), "r")    # 读取文件夹的info.json文件，获取任务详情
    info = json.load(get_info)
    get_info.close()
    file_list = os.listdir(task_path)    # 获取目标文件夹下的文件列表
    file_list.remove("info.json")    # 删除列表中的“info.json”元素，这不是需要打印的文件
    for file_name in file_list:
        copies = int(info[file_name]["copies"])    # 获取打印份数
        printing_copies = 1
        for j in range(copies):
            try:
                win32api.ShellExecute(0, 'print', os.path.join(task_path, file_name), '', '', 1)    # 调用默认软件实施打印
            except Exception:
                print("printer:调用相关文档程序失败，请将福昕阅读器作为打开PDF的默认程序，并保证您的计算机的默认打印机"
                      "不是类似于pdf打印机的这种文件打印机")
                return False
            else:
                print('printer:正在打印第' + str(printing_copies) + "份" + file_name)
                printing_copies = printing_copies + 1
    print(WHERE, "所有文件打印完毕！")
    return True


def print_local_task(task_path):
    local_files_list=os.listdir(task_path)
    for file_name in local_files_list:
        print("printer", file_name)
        if re.match(r'.*.((pdf)|(doc)|(docx))$', file_name):
            try:
                win32api.ShellExecute(0, 'print', task_path + file_name, '', '', 1)  # 调用默认软件实施打印
            except Exception:
                print("printer:调用相关文档程序失败，请将福昕阅读器作为打开PDF的默认程序、安装office软件。并保证您的"
                      "计算机的默认打印机不是类似于pdf打印机的这种文件打印机")
            time.sleep(5)    # 提交任务需要时间,最好的方法是在短暂等待之后获取文件的状态，查看是否被占用
            os.remove(task_path + file_name)


'''
os.chdir('C:/printer/received/18796282979')
print(os.getcwd())
print_files('C:/printer/received/18796282979/22942700')
# '''
