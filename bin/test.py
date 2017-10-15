from PyQt5.QtWidgets import *
import sys


#class MyWindow(QWidget)
app = QApplication(sys.argv)
w1 = QWidget()
w1.resize(800,400)
w1.setWindowTitle("云打印")
w1.show()
sys.exit(app.exec_())