import win32api
import win32print

printer_name = win32print.GetDefaultPrinter()
print("默认打印机", printer_name)
handle_printer = win32print.OpenPrinter(printer_name)  # 获取打印机句柄
printer_info = win32print.GetPrinter(handle_printer, 2)  # 调用相关函数进行信息查询
for k in printer_info:
    print(k, printer_info[k])
task_list = win32print.EnumJobs(handle_printer, 0, 10)  # 参数（句柄，编文档号，枚举条数）
print(task_list)


import bin.my_lib.data_sqlite as db
res = db.execute('SELECT * FROM KEY_VALUE')
print('res:', res)