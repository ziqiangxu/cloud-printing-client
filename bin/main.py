# 主程序
# 已知漏洞：如果一个用户有多个文件，中间可能夹带其他打印机的任务
import getpass
import json
import os
import sys
import bin.printer as printer
import re
import win32api
import time
import threading
import bin.receiver3 as receiver
bin_path = os.getcwd()[:-4]
sys.path.append(bin_path)
print(sys.path)


def get_json(json_path,json_name):
    old_path = os.getcwd()  # 记录原来所在目录
    os.chdir(json_path)  # 切换到任务路径
    read_config = open(json_name, 'r')
    content = json.load(read_config)
    read_config.close()
    os.chdir(old_path)  # 回到原来的目录
    return content
def change_json(json_path,json_name,json_dict):
    old_path=os.getcwd()#记录原来所在目录
    os.chdir(json_path)#切换到任务路径
    wirte_json = open(json_name, "w")
    json.dump(json_dict, wirte_json)
    wirte_json.close()
    os.chdir(old_path)#回到原来的目录
    return '信息更新成功'
######################################################
user_name = getpass.getuser()    # 获取当前用户名Get the username
print("main:当前电脑用户名是："+user_name)
WORK_PATH = "c:\\printer\\received\\"
os.chdir(WORK_PATH)    # 把当前目录切换到/printer/received下
print("main:当前工作目录是"+os.getcwd())
# config = get_json("c:\\printer",'config.json')    # 从config.json文件读取配置信息
# print(config)    # 显示当前的配置信息
# 线程1：接收服务器的文件


class ThreadReceiver(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        receiver.start()
        print("main:开始线程："+ self.name)


receiver1 = ThreadReceiver(1, "receiver")
receiver1.start()
# 线程2：打印接收完毕的文件


def print_received_files():
    while True:
        try:
            user_list = os.listdir(WORK_PATH)  # 持续地获取传输文件夹的文件列表
            print("main:当前收到的文件有：\n", user_list)
            for user in user_list:
                regist_user = re.match('^1[0-9]{10}$', user)  # 判断文件夹是否符合命名规则
                task_list = os.listdir(os.path.join(WORK_PATH, user))
                for task in task_list:
                    print("main:正在扫描received_files")
                    file_list = os.listdir(os.path.join(WORK_PATH, user, task))
                    if regist_user and ('info.json' in file_list):
                        task_abspath = os.path.join(WORK_PATH, user, task)
                        info = get_json(task_abspath, 'info.json')  # 获取info信息
                        status = info['user']['status']
                        print("-------------------------")
                        if status == 'received':  # 判断文件是否传输完毕
                            print("main:received")
                            print("main:" + task + "的所有文件已经传输完毕，开始打印")
                            # change_json("C:\\printer", "config.json", config)
                            print(task_abspath)
                            printer.print_files(task_abspath + '\\')
                            # 打印task目录下的文档，只需向printer函数提交一个绝对路径就可
                            # 以打印该目录所有的文档
                            message = '用户' + task + '已经打印'
                            win32api.MessageBox(0, message, '提示信息', 1)
                            info['user']['status'] = 'printing'  # 把处理状态修改为printing
                            print('main:当前目录为：', os.getcwd())
                            change_json(task_abspath, 'info.json', info)  # 写入info信息，修改status的状态
                        elif status == 'receiving':
                            print("main:用户:%s的文件尚未传输完毕，暂不打印" % task)
                        elif status == 'printed':
                            print("main:用户:%s的文件打印完毕，无需处理" % task)
                        """
                        elif status == 'printing':
                            if printer.task():
                                print("main:用户:%s的文件正在打印，无需处理" % task)
                            else:
                                print("main:用户:%s的文件打印完毕，移至printed文件夹" % task)
                                printed_info = get_json(os.path.join(WORK_PATH, user, task), "info.json")
                                serial_number = printed_info["serial_number"]
                                os.mkdir("C:\\printer\\printed\\" + serial_number)  # 创建用任务号命名的文件夹
                                shutil.move(os.path.join(WORK_PATH, user, task),
                                            "c:\\printer\\printed\\%s" % serial_number)   
                    """
        except:
            print("main:打印收到文件出错")
        time.sleep(10)  # 两秒扫描一次文件目录


class ThreadPrintReceived (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        print ("main:开始线程：" + self.name)
        print_received_files()


print_thread1 = ThreadPrintReceived(1, "print_receive_files")
print_thread1.start()


# 线程3：打印local_task的文件


def print_local_files():
    while True:
        printer.print_local_task("c:\\printer\\local_task\\")
        time.sleep(2)    # 2秒扫描一次文件夹


class ThreadPrintLocal (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        print ("main:开始线程：" + self.name)
        print_local_files()


local_print_thread1 = ThreadPrintLocal(1, "print_local_files")
local_print_thread1.start()
