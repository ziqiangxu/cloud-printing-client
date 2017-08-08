import os
import json
import time
import win32print,win32api
def task():#获取默认打印机的工作状态
    printer_name = win32print.GetDefaultPrinter()
    handle_printer = win32print.OpenPrinter(printer_name)#获取打印机句柄
    printer_info = win32print.GetPrinter(handle_printer, 2)#调用相关函数进行信息查询
    task_list=win32print.EnumJobs(handle_printer,0,10)#参数（句柄，编文档号，枚举条数）
    return printer_info["cJobs"]  # 获取当前打印机任务数目
def __doc__():
    return("这是打印文档的核心函数，需要传入打印文件夹的路径作为参数")
def print_files(file_path):#本函数将根据info.json要求打印目标文件夹的所有文件
    get_info=open(file_path+"/info.json","r")#读取文件夹的info.json文件，获取任务详情
    info=json.load(get_info)
    get_info.close()
    #os.chdir(file_path)#将当前工作目录切换到目标目录
    file_list=os.listdir(file_path)#获取目标文件夹下的文件列表
    file_list.remove("info.json")#删除列表中的“info.json”元素，这不是需要打印的文件
    for file_name in file_list:
        copies=info[file_name]["copies"]#获取打印份数
        for j in range(copies):
            try:
                win32api.ShellExecute(0, 'print', file_path + file_name, '', '', 1)#调用默认软件实施打印
            except IndentationError:
                print('调用相关文档程序失败，请将福昕阅读器作为打开PDF的默认程序')
            else:
                print('正在打印' + file_name)
#os.chdir('C:/printer/received')
#print(os.getcwd())
#print_files('C:/printer/received/18796282979/')