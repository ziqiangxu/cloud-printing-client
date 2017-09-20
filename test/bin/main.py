# coding = gbk
# 主程序
# 已知漏洞：如果一个用户有多个文件，中间可能夹带其他打印机的任务
import getpass
import os
import printer
import time
import threading
import receiver as receiver
import json_read_write as json_wr
import printer as printer

user_name = getpass.getuser()
WHERE = "main:"
print(WHERE, "当前电脑用户名是："+user_name)
WORK_PATH = "c:\\printer\\received\\"


class ThreadReceiver(threading.Thread):    # 线程1：接收服务器的文件
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        receiver.start()
        print("main:开始线程："+ self.name)
receiver1 = ThreadReceiver(1, "receiver1")
receiver1.start()


# 线程2：打印接收完毕的文件
def print_received_files():
    while True:
        try:
            user_list = os.listdir(WORK_PATH)
            for user_id in user_list:
                user_path = os.path.join(WORK_PATH, user_id)
                task_list = os.listdir(user_path)
                for task_id in task_list:
                    task_path = os.path.join(user_path, task_id)
                    if "info.json" in os.listdir(task_path):
                        info = json_wr.read(os.path.join(task_path, "info.json"))
                        status = info["user"]["status"]
                        if status == "received":
                            print(WHERE, "用户%s的%s任务文件开始打印" % (user_id, task_id))
                            if printer.print_files(task_path):
                                print(WHERE, "用户%s的%s任务文件提交成功" % (user_id, task_id))
                            else:
                                info["user"]["status"] = "error"
                                json_wr.write(os.path.join(task_path, "info.json"), info)
                        elif status == "printing":
                            print(WHERE, "用户%s的%s任务文件已提交" % (user_id, task_id))
                        else:
                            print(WHERE,"用户%s的%s任务状态异常" % (user_id, task_id))
        except:
            print(WHERE, "用户%s的%s任务打印失败" % (user_id, task_id))

        time.sleep(5)


class ThreadPrintReceived (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        print(WHERE, "开始线程：" + self.name)
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
