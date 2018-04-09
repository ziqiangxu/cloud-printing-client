import time
import threading
import bin.my_lib.receiver3 as receiver

'''
def print_local_files():
    while True:
        printer.print_local_task("c:\\printer\\local_task\\")
        time.sleep(2)    # 2秒扫描一次文件夹


def print_received_files():
    while True:
        try:
            user_list = os.listdir(WORK_PATH)  # 持续地获取传输文件夹的文件列表
            print("main:当前收到的文件有：\n", user_list)
            for user in user_list:
                registered_user = re.match('^1[0-9]{10}$', user)  # 判断文件夹是否符合命名规则
                task_list = os.listdir(os.path.join(WORK_PATH, user))
                for task in task_list:
                    print("main:正在扫描received_files")
                    file_list = os.listdir(os.path.join(WORK_PATH, user, task))
                    if registered_user and ('info.json' in file_list):
                        task_abspath = os.path.join(WORK_PATH, user, task)
                        info = json_read_write.read(os.path.join(task_abspath, "info.json"))   # 获取info信息
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
                            message = '用户%s已经打印' % task
                            win32api.MessageBox(0, message, '提示信息', 1)
                            info['user']['status'] = 'printing'  # 把处理状态修改为printing
                            print('main:当前目录为：', os.getcwd())
                            # change_json(task_abspath, 'info.json', info)
                            json_read_write.write(os.path.join(task_abspath, "info.json"), info)  # 写入info信息，修改status的状态
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
'''


class ThreadReceiver(threading.Thread):
    # 下载模块
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def receiver(self):
        # 每10秒从服务器获取一次文件
        while True:
            print("开始执行下载程序")
            receiver.start()
            print("下载程序执行完毕")
            time.sleep(10)

    def run(self):
        self.receiver()
        print("main:开始线程："+ self.name)


'''
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
'''

# 线程1：接收服务器的文件
# receiver1 = ThreadReceiver(1, "receiver")
# receiver1.start()
# 线程2：打印接收完毕的文件
# print_thread1 = ThreadPrintReceived(1, "print_receive_files")
# print_thread1.start()
# 线程3：打印local_task的文件
# local_print_thread1 = ThreadPrintLocal(1, "print_local_files")
# local_print_thread1.start()