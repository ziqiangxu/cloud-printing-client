# cloud_printer
解决校园打印店用户等待电脑，而不是等待打印机的问题。即在用户向打印机提交任务的时候容易出现阻塞，拔插U盘、登录邮箱或者登录QQ，寻找文件，U盘有中病毒的风险，QQ容易出现锁定。为了更加高效地利用打印机，我们不一定需要使用打印店的PC来提交打印任务。通过这个程序，可以自动打印移动设备或者其他网络设备发送过来的文件。但这只是实现功能上的原型,目前只完成了本地端的实现。本程序也开发了自动打印指定文件夹下（C:\printer\local_task）的功能。在本程序运行时，您只需要把文件拖到这个目录下，就能自动打印哦。    
使用环境：    
Microsoft Windows操作系统    
Python3 [下载地址](https://www.python.org/)    
对应版本扩展库pywin32 [下载地址](https://sourceforge.net/projects/pywin32/files/pywin32/Build%20221/)
可能pywin32的下载地址国内无法访问，可以在仓库的setup文件夹获取3.6版本的安装包
> 开发时使用Python3.6
安装方法：    
执行setup目录下的setup.py    
使用方法：    
安装完之后执行c:\printer\bin\main.py即可    
欢迎来件交流[我的邮箱](mailto:ziqiang_xu@yeah.net)
