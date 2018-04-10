import bin.my_lib.data_sqlite as data_sqlite
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import PyQt5.uic as uic
import sys
import os
import test_files.mainwindow as main_window


class TestWindow(QMainWindow):
    def __init__(self):
        super(TestWindow, self).__init__()
        print(os.getcwd())
        ui = main_window.Ui_MainWindow()
        ui.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = TestWindow()
    w.show()
    sys.exit(app.exec_())