from PyQt5.QtCore import *
import sys
from PyQt5.QtWidgets import *
import bin.settings as settings


class SettingWindow(QWidget):
    def __init__(self, parent=None):
        # super(SettingWindow, self).__init__(parent)
        super().__init__()
        self.build_gui()
        # 创建表格布局
        layout1 = QFormLayout()
        self.setLayout(layout1)

        # 填充标签和字段
        self.auto_download = QPushButton(self)
        layout1.addWidget(self.auto_download)
        if settings.AUTO_DOWNLOAD_TASKS:
            self.auto_download.setText("开")
        else:
            self.auto_download.setText("关")
        layout1.addRow(QLabel("自动下载任务"), self.auto_download)

    def build_gui(self):
        self.setWindowTitle("设置")
