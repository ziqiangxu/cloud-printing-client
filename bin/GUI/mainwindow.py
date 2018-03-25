import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from urllib.request import urlopen

bin_path = os.getcwd()[:-4]  # bin作为工作目录
print("工作目录为：", bin_path)
sys.path.append(bin_path)
import bin.my_lib.data_sqlite as data_sqlite
import bin.my_lib.printer as printer
import bin.units as units
import bin.settings as settings

task_dict = {}
WHERE = 'mainwindow.py'


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("cloud_print_client")
        windows_width = 800
        windows_height = 400
        self.setFixedSize(windows_width, windows_height)
        # self.setWindowFlag(Qt.FramelessWindowHint)
        # ** 界面布局 ** #
        # 打印机名称
        printer_name = QLabel(self)
        printer_name.setText("HP-Office-8100Pro")

        # 电话
        tel = QLabel(self)
        tel.setText("手机:%s" % settings.SHOP_TEL)

        # 创建Tabs
        tabs = QTabWidget(self)
        tabs.tab1 = QWidget()
        tabs.tab2 = QWidget()
        tabs.tab3 = QWidget()
        tabs.tab4 = QWidget()
        tabs.addTab(tabs.tab1, "等待处理")
        tabs.addTab(tabs.tab2, "已处理")
        tabs.addTab(tabs.tab3, "错误")
        #self.buildGUI()

        # 控件位置和大小
        printer_x = 10
        printer_y = 10
        printer_name.move(printer_x, printer_y)
        printer_name.setFixedSize(150, 15)

        tel.move(printer_x + printer_name.width(),
                 printer_name.y())
        tel.setFixedSize(100, 15)

        tabs.move(printer_x,
                  printer_y + printer_name.height() + 10)
        tabs.setFixedSize(windows_width - 20,
                          windows_height - tabs.y() - 20)

        # ** 创建QListWidget控件 ** #
        self.waiting_tasks = QListWidget(tabs.tab1)
        self.waiting_tasks.setFixedSize(windows_width - 30, tabs.tab1.height() - 160)
        self.printed_tasks = QListWidget(tabs.tab2)
        self.printed_tasks.setFixedSize(windows_width - 30, tabs.tab1.height() - 160)

        # 填充tabs
        self.fillTabs()
        # 每5秒刷新一次tabs内容
        tabs_flasher = QTimer(self)
        tabs_flasher.timeout.connect(self.fillTabs)
        tabs_flasher.start(5000)

        # ** 信号-槽绑定 ** #
        self.waiting_tasks.itemDoubleClicked.connect(self.double_click)
        self.printed_tasks.itemDoubleClicked.connect(self.double_click)
        # quit.clicked.connect(self.test)

        # ** 开启其它模块 ** #
        # 启动文件接收器线程，已知问题，下载线程无法在程序退出后自动停止
        # commands.kill_all_threading()
        '''
        task_receiver = units.ThreadReceiver(1, "task_receiver")
        task_receiver.start() # python线程的停止需要自己实现
        '''

    # ** 普通成员函数 ** #

    def buildGUI(self):
        tabs.addTab(self.tabs.tab4, "警告")

    def fillTabs(self):
        # 填充tabs
        tab1 = self.waiting_tasks
        tab2 = self.printed_tasks
        tab1.clear()
        tab2.clear()
        print(WHERE, "刷新tabs")
        # 获取received的任务
        tasks = data_sqlite.task_list("SELECT task_ID,local_path,name,tel FROM task WHERE status_code='received'")
        for i in tasks:
            content = "任务号：" + str(i[0] + "    电话：" + i[3] + "    姓名：" + i[2] + "    下载完毕")
            tab1.addItem(content)
            task_dict[i[0]] = {"local_path": i[1]}
        # 获取downloading的任务
        tasks = data_sqlite.task_list("SELECT task_ID,local_path,name,tel FROM task WHERE status_code='receiving'")
        for i in tasks:
            content = "任务号：" + str(i[0] + "    电话：" + i[3] + "    姓名：" + i[2] + "    正在下载")
            tab1.addItem(content)
            task_dict[i[0]] = {"local_path": i[1]}
        # 获取printing状态任务
        tasks = data_sqlite.task_list("SELECT task_ID,local_path,name,tel FROM task WHERE status_code='printing'")
        for i in tasks:
            content = "任务号：" + i[0] + "    电话：" + i[3] + "    姓名：" + i[2] + "    已处理"
            tab2.addItem(content)

    def test(self):
        print(WHERE, "Test OK!")

    # ** 槽函数 ** #
    def double_click(self, item):
        # 双击事件
        where = self.waiting_tasks.currentRow()
        task_ID = item.text()[4:12]  # 取出任务号,应该进行修改，防止文本变更时引起程序更改
        # 状态验证
        status_code = data_sqlite.task_list("SELECT status_code FROM task WHERE task_ID='%s'" % task_ID)
        print(status_code[0][0], "OK")
        if not status_code[0][0] == 'received':
            QMessageBox.information(self, "提示！", "本任务还没有下载好或者已经处理！")
            return False
        local_path = task_dict[task_ID]["local_path"]
        print(local_path)
        if printer.print_files(local_path):  # 打印文件
            data_sqlite.execute("UPDATE task SET status_code='printing' WHERE task_ID='%s'" % task_ID)
            self.printed_tasks.addItem(item.text())
        else:
            data_sqlite.execute("UPDATE task SET status_code='warning' WHERE task_ID='%s'" % task_ID)
        self.waiting_tasks.takeItem(where)
        try:
            url = settings.SITE + "/update_task/?task_ID=%s&status=20" % task_ID
            urlopen(url)
        except:
            print(WHERE, "修改任务在服务器的状态为20失败")
        # QMessageBox.information(self, "提示", "开始打印任务%s" % item.text())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())    # 结束程序之前需要关闭其它线程，如：下载线程

