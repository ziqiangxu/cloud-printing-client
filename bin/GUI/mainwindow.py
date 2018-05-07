import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from urllib.request import urlopen

bin_path = os.getcwd()[:-4]  # bin作为工作目录
print(__file__, "工作目录为：", bin_path)
sys.path.append(bin_path)
import bin.my_lib.data_sqlite as data_sqlite
import bin.units as units
import bin.settings as settings
import bin.GUI.SubWindows as SubWindows
import bin.my_lib.receiver3 as receiver

task_dict = {}
WHERE = 'MainWindow.py'
CONFIG = settings.load_config()


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # 创建相关控件，在主界面创建控件必须在初始化函数添加
        self.tabs = QTabWidget(self)
        self.tabs.waiting = QWidget()
        self.tabs.printed = QWidget()
        self.tabs.error = QWidget()
        self.tabs.warning = QWidget()
        self.printer_name = QComboBox(self)  # 打印机名称显示控件
        self.tel = QLabel(self)  # 手机号码显示控件
        self.waiting_tasks = QListWidget(self.tabs.waiting)  # 等待打印列表
        self.printed_tasks = QListWidget(self.tabs.printed)  # 已处理列表
        self.setting = QPushButton(self)  # 设置按钮
        # self.testButton = QPushButton(self)
        # 对界面进行更细微的控制
        self.build_gui()

        # 登录
        self.login()

        # 填充tabs
        self.fill_tabs()
        # 每5秒刷新一次tabs内容
        tabs_flasher = QTimer(self)
        tabs_flasher.timeout.connect(self.fill_tabs)
        tabs_flasher.start(5000)

        # ** 信号-槽绑定 ** #
        self.waiting_tasks.itemDoubleClicked.connect(self.double_click)
        self.printed_tasks.itemDoubleClicked.connect(self.double_click)
        self.waiting_tasks.itemClicked.connect(self.show_in_explorer)
        self.printer_name.currentTextChanged.connect(self.recent_printer_changed)
        self.setting.clicked.connect(self.show_setting_window)
        # self.testButton.clicked.connect(self.test)
        # quit.clicked.connect(self.test_files)

        # ** 开启其它模块 ** #
        # 启动文件接收器线程，已知问题，下载线程无法在程序退出后自动停止
        # commands.kill_all_threading()
        if CONFIG["auto_download_tasks"]:
            print(WHERE, "自动下载任务 开启")
            self.task_receiver = units.ThreadReceiver(1, "task_receiver")
            self.task_receiver.start() # python线程的停止需要自己实现
        else:
            print(WHERE, "自动下载任务 未开启")
            receiver.start()

    # ** 普通成员函数 ** #

    def login(self):
        if True:
            # 打开设置窗口，填写账号
            self.w = SubWindows.SettingWindow(self)
            if self.w.fields['shop_tel'].text() == '18796282979':
                self.w.fields['shop_tel'].setText("请在此处输入手机号")
                self.w.fields["shop_tel"].selectAll()
            self.w.show()

    def show_setting_window(self):
        self.w = SubWindows.SettingWindow(self)
        self.w.__init__(self)
        self.w.show()

    def build_gui(self):
        self.tabs.addTab(self.tabs.waiting, "等待处理")
        self.tabs.addTab(self.tabs.printed, "已处理")
        self.tabs.addTab(self.tabs.error, "错误")
        self.setWindowTitle("cloud_print_client")
        window_width = 800
        window_height = 400
        self.setFixedSize(window_width, window_height)
        # ** 界面布局 ** #
        self.printer_name.addItem(CONFIG['recent_printer'])
        self.printer_name.addItems(settings.PRINTER_LIST)
        # 电话
        self.tel.setText("手机:%s" % CONFIG["shop_tel"])

        # 控件位置和大小
        printer_x = 10
        printer_y = 10
        self.printer_name.move(printer_x, printer_y)
        self.printer_name.setFixedSize(250, 20)

        self.tel.move(printer_x + self.printer_name.width(),
                 self.printer_name.y())
        self.tel.setFixedSize(100, 15)

        self.setting.move(400, 10)
        self.setting.setText("设置")

        self.tabs.move(printer_x,
                       printer_y + self.printer_name.height() + 10)
        self.tabs.setFixedSize(window_width - 20,
                               window_height - self.tabs.y() - 20)

        # ** 创建QListWidget控件 ** #
        self.waiting_tasks.setFixedSize(window_width - 30, self.tabs.waiting.height() - 160)
        self.printed_tasks.setFixedSize(window_width - 30, self.tabs.waiting.height() - 160)

    def fill_tabs(self):
        # 填充tabs
        waiting = self.waiting_tasks
        printed = self.printed_tasks
        waiting.clear()
        printed.clear()
        print(WHERE, "刷新tabs")
        # 获取received的任务
        tasks = data_sqlite.task_list("SELECT task_ID,local_path,name,tel FROM task WHERE status_code='received'")
        for i in tasks:
            content = "任务号：" + str(i[0] + "    电话：" + i[3] + "    姓名：" + i[2] + "    下载完毕")
            waiting.addItem(content)
            task_dict[i[0]] = {"local_path": i[1]}
        # 获取downloading的任务
        tasks = data_sqlite.task_list("SELECT task_ID,local_path,name,tel FROM task WHERE status_code='receiving'")
        for i in tasks:
            content = "任务号：" + str(i[0] + "    电话：" + i[3] + "    姓名：" + i[2] + "    正在下载")
            waiting.addItem(content)
            task_dict[i[0]] = {"local_path": i[1]}
        # 获取printing状态任务
        tasks = data_sqlite.task_list("SELECT task_ID,local_path,name,tel FROM task WHERE status_code='printing'")
        for i in tasks:
            content = "任务号：" + i[0] + "    电话：" + i[3] + "    姓名：" + i[2] + "    已处理"
            printed.addItem(content)

    def test(self):
        print(WHERE, "Test OK!")
        self.w = QFileDialog(self)
        if self.w.exec() == QDialog.Accepted:
            print(WHERE, self.w.selectedFiles())
        else:
            self.w.close()

    # 重写的事件
    def closeEvent(self, QCloseEvent):
        self.task_receiver.stop()  # 停止下载线程
        print(WHERE, "主窗口关闭，停止下载线程")
        QCloseEvent.accept()

    # ** 槽函数 ** #
    def double_click(self, item):
        # 双击事件
        where = self.waiting_tasks.currentRow()
        task_id = item.text()[4:12]  # 取出任务号,应该进行修改，防止文本变更时引起程序更改
        # 状态验证
        status_code = data_sqlite.task_list("SELECT status_code FROM task WHERE task_ID='%s'" % task_id)
        print(status_code[0][0], "OK")
        if not status_code[0][0] == 'received':
            QMessageBox.information(self, "提示！", "本任务还没有下载好或者已经处理！")
            return False
        local_path = task_dict[task_id]["local_path"]
        print(WHERE, local_path)
        if CONFIG["os"] == "Windows":
            import bin.my_lib.printer2 as printer
        else:
            print(WHERE, "暂不支持非Windows系统")
            return False
        if printer.print_files(local_path, self.printer_name.currentText()):  # 处理一个任务
            data_sqlite.execute("UPDATE task SET status_code='printing' WHERE task_ID='%s'" % task_id)
            self.printed_tasks.addItem(item.text())
        else:
            data_sqlite.execute("UPDATE task SET status_code='warning' WHERE task_ID='%s'" % task_id)
        self.waiting_tasks.takeItem(where)
        try:
            url = CONFIG["site"] + "/update_task/?task_ID=%s&status=20" % task_id
            urlopen(url)
        except:
            print(WHERE, "修改任务在服务器的状态为20失败")
        # QMessageBox.information(self, "提示", "开始打印任务%s" % item.text())

    def recent_printer_changed(self):
        res = data_sqlite.execute("UPDATE KEY_VALUE SET VALUE='%s' WHERE KEY='recent_printer'"
                                  % self.printer_name.currentText())
        if not res:
            return False
        return True

    def show_in_explorer(self):
        cmd = 'explorer.exe c:/printer/received'
        cmd = cmd.replace('/', '\\')
        print(WHERE, "打开浏览器，执行的命令：", cmd)
        os.system(cmd)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())    # 结束程序之前需要关闭其它线程，如：下载线程

