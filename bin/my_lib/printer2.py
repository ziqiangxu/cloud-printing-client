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
import re
import bin.my_lib.json_read_write as json_rw
import bin.settings as settings
WHERE = "lib/printer2.py"
CONFIG = settings.load_config()


def __doc__():
    return "receiver:这是打印文档的核心函数，需要传入打印文件夹的路径作为参数"


def print_file(path, duplex, color, copies, printer_name):
    """
    :param path: PDF文件路径
    :param duplex: 单双面控制 duplex双面 duplexshorrt双面短边翻转 duplexlong双面长边翻转 simplex单面
    :param color: 颜色 color彩色 monochrome单色（目前无法控制）
    :param copies: 份数 整数
    :param printer_name: 打印机名字
    :return: bool
    """
    # 调用系统命令的时候打印机名、打印设置、文件名需要用双引号包裹
    cmd = CONFIG["workplace"] + '\\SumatraPDF\\SumatraPDF.exe ' \
                                '-print-to "%s" ' \
                                '-print-settings "%s,%s,%sx" ' \
                                '"%s"' % (printer_name,
                                            duplex, color, copies,
                                            path)
    print(WHERE, "执行命令：", cmd)
    cmd.replace('/', '\\')
    os.system(cmd)


def print_files(task_path='', printer_name=''):
    # 本函数将根据info.json要求打印目标文件夹的所有文件【绝对路径】
    task_path = task_path.replace('/', '\\')
    print(WHERE, "要处理的目录：", task_path)
    info = json_rw.read(os.path.join(task_path, "info.json"))    # 读取文件夹的info.json文件，获取任务详情
    if not info:
        print_files(WHERE, "读取info.json文件失败")
        return False
    file_list = os.listdir(task_path)    # 获取目标文件夹下的文件列表
    file_list.remove("info.json")    # 删除列表中的“info.json”元素，这不是需要打印的文件
    for file_name in file_list:
        info_file = info.get(file_name)
        # 确认任务列表有此文件
        if not info_file:
            next(file_name)
        # 调起打印单个文件的函数
        file_path = os.path.join(task_path, file_name)
        try:
            duplex = info_file["duplex"]
            color = info_file["color"]
            copies = info_file["copies"]
        except:
            print(WHERE, "info文件有问题，缺少某些参数")
            return False
        print_file(file_path, duplex, color, copies, printer_name)
    print(WHERE, task_path,"所有文件打印完毕！")
    return True


"""
print_file("C:\\printer\\SumatraPDF\\1.pdf",
           "simplex", "color", 2,
           "HP00E810 (HP Officejet Pro 8100)")
"""
"""
print_files("C:\\printer\\received\\18796282979\\97192937", "HP00E810 (HP Officejet Pro 8100)")
# """
