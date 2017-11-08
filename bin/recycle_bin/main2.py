# 主程序
# 已知漏洞：如果一个用户有多个文件，中间可能夹带其他打印机的任务
import getpass
import os
import sys
bin_path = os.getcwd()[:-4]  # cloud_printing_client作为工作目录
sys.path.append(bin_path)
print("类库文件扫描路径", sys.path)
import threading
import bin.recycle_bin.manager as manager

user_name = getpass.getuser()    # 获取当前用户名Get the username
print("main:当前电脑用户名是："+user_name)


class ThreadReceiver(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        manager.receiver()
        print("main:开始线程："+ self.name)


class ThreadPrintReceived (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        print ("main:开始线程：" + self.name)
        manager.print_received_files()


class ThreadPrintLocal (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        print ("main:开始线程：" + self.name)
        manager.print_local_files()


# 线程1：接收服务器的文件
receiver1 = ThreadReceiver(1, "receiver")
receiver1.start()
# 线程2：打印接收完毕的文件
# print_thread1 = ThreadPrintReceived(1, "print_receive_files")
# print_thread1.start()
# 线程3：打印local_task的文件
# local_print_thread1 = ThreadPrintLocal(1, "print_local_files")
# local_print_thread1.start()