from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import os


class NotPrint(QWidget):
    def __init__(self, parent=None):
        super(NotPrint, self).__init__(parent)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.status = self.statusBar()
        self.status.showMessage("This is toolbar tips")
        self.setWindowTitle("cloud_print_client")
        windows_width = 800
        windows_height = 400
        self.setFixedSize(windows_width, windows_height)

        # Printer name
        printer_name = QLabel(self)
        printer_name.setText("显示默认打印机名称:HP-8100Pro")

        # Tel
        tel = QLabel(self)
        tel.setText("ID:18796282979")

        # Tabs
        tabs = QTabWidget(self)
        tabs.tab1 = QWidget()
        tabs.tab2 = QWidget()
        tabs.addTab(tabs.tab1, "未打印")
        tabs.addTab(tabs.tab2, "已打印")

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

        # 填充tabs

        def double_click(item):
            where = printing_tasks.currentRow()
            print(where, item.data(1))
            printed_tasks.addItem(item.text())
            printing_tasks.takeItem(where)
            # QMessageBox.information(self, "提示", "开始打印任务%s" % item.text())

        printing_tasks = QListWidget(tabs.tab1)
        printed_tasks = QListWidget(tabs.tab2)
        printing_tasks.setFixedSize(windows_width - 20, tabs.tab1.height())
        printed_tasks.setFixedSize(windows_width - 20, tabs.tab1.height())
        tasks = os.listdir("/printer/received/18796282979")
        index = 0
        for i in tasks:
            printing_tasks.addItem(i)
            item_instance = printing_tasks.item(index)
            item_instance.setData(1, "test_files%d" % index)
            index += 1
        printing_tasks.itemDoubleClicked.connect(double_click)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())