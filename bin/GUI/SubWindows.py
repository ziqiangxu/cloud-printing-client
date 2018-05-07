import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import bin.settings as settings
import bin.my_lib.json_read_write as json_rw
import bin.my_lib.data_sqlite as db
CONFIG = settings.load_config()
CONFIG_PATH = CONFIG["config_path"]


class SettingWindow(QWidget):
    def __init__(self, parent=None):
        # super(SettingWindow, self).__init__(parent)
        super().__init__()
        # 创建表格布局
        self.layout1 = QFormLayout()
        self.layout2 = QVBoxLayout()
        self.setLayout(self.layout2)
        self.layout2.addLayout(self.layout1)

        # 填充标签和字段
        self.auto_download = QPushButton(self)
        self.fields = {}
        self.fields['shop_tel'] = QLineEdit(self)
        self.fields['password'] = QLineEdit(self)
        self.submit = QPushButton(self)
        self.layout1.addWidget(self.auto_download)
        if CONFIG["auto_download_tasks"] == 'True':
            self.auto_download.setText("开")
        else:
            self.auto_download.setText("关")
        self.auto_download.clicked.connect(self.auto_download_toggle)
        self.layout1.addRow(QLabel("自动打印"), self.auto_download)
        self.layout1.addRow(QLabel('账号'), self.fields['shop_tel'])
        self.layout1.addRow(QLabel('密码'), self.fields['password'])
        self.build_gui()
        self.signal_slot()

    def update_settings(self):
        for i in self.fields.keys():
            value = self.fields[i].text()
            # 执行更新操作
            db.execute("UPDATE KEY_VALUE SET VALUE='%s' WHERE KEY='%s'" % (value, i))
        self.fields['password'].setText('******')

    def signal_slot(self):
        self.submit.clicked.connect(self.update_settings)

    def build_gui(self):
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.fields['shop_tel'].setText(CONFIG['shop_tel'])
        self.fields['password'].setText('******')
        self.submit.setText('提交')
        self.layout2.addWidget(self.submit)
        self.setWindowTitle("设置")

    def auto_download_toggle(self):
        if self.auto_download.text() == "开":
            res = db.execute("UPDATE KEY_VALUE SET VALUE='False' WHERE KEY='auto_download_tasks'")
            if not res:
                print(__file__, 'failed to save')
                return False
            self.auto_download.setText('关')
            return True
        else:
            res = db.execute("UPDATE KEY_VALUE SET VALUE='True' WHERE KEY='auto_download_tasks'")
            if not res:
                print(__file__, 'failed to save')
                return False
            self.auto_download.setText('开')
            return True

