import win32process
import win32
import win32api
#一种调用程序的方法
#win32process.CreateProcess('C:\\Program Files (x86)\\Adobe\\Acrobat Reader DC\\Reader\\AcroRd32.exe',
#                          '/p /h C:\\printer\\110.pdf',None,None,0,win32process.CREATE_NO_WINDOW,None,None,win32process.STARTUPINFO())
#一种可以后台运行程序的方法-----最后一个参数改为0