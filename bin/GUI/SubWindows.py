from PyQt5.QtCore import *
import sys
from PyQt5.QtWidgets import *


class SettingWindow(QMainWindow):
    def __init__(self, parent=None):
        # super(SettingWindow, self).__init__(parent)
        super().__init__()
        self.build_gui()

    def build_gui(self):
        self.setWindowTitle("设置")
