import os
from PyQt5.QtWidgets import *
import bin.settings as settings
import bin.my_lib.json_read_write as json_rw
CONFIG = settings.load_config()
CONFIG_PATH = CONFIG["config_path"]
WHERE = "GUI/SubWindows"


class SettingWindow(QWidget):
    def __init__(self, parent=None):
        # super(SettingWindow, self).__init__(parent)
        super().__init__()
        # 创建表格布局
        layout1 = QFormLayout()
        self.setLayout(layout1)

        # 填充标签和字段
        self.auto_download = QPushButton(self)
        layout1.addWidget(self.auto_download)
        if CONFIG["auto_download_tasks"]:
            self.auto_download.setText("开")
        else:
            self.auto_download.setText("关")
        self.auto_download.clicked.connect(self.auto_download_toggle)
        layout1.addRow(QLabel("自动下载任务"), self.auto_download)
        self.build_gui()

    def build_gui(self):
        self.setWindowTitle("设置")

    def auto_download_toggle(self):
        if self.auto_download.text() == "开":
            try:
                config = json_rw.read(CONFIG_PATH)
                config["auto_download_tasks"] = False
                json_rw.write(CONFIG_PATH, config)
            except:
                print(WHERE, "写入config文件出错")
            self.auto_download.setText('关')
        else:
            try:
                config = json_rw.read(CONFIG_PATH)
                config["auto_download_tasks"] = True
                json_rw.write(CONFIG_PATH, config)
            except:
                print(WHERE, "写入config文件出错")
            self.auto_download.setText('开')

