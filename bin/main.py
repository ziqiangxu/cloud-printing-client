import getpass
import json
import os
from source import printer
import re
import win32api
import time
def get_json(json_path,json_name):
    old_path = os.getcwd()  # 记录原来所在目录
    os.chdir(json_path)  # 切换到任务路径
    read_config = open(json_name, 'r')
    content = json.load(read_config)
    read_config.close()
    os.chdir(old_path)  # 回到原来的目录
    return content
def change_json(json_path,json_name,json_dict):
    old_path=os.getcwd()#记录原来所在目录
    os.chdir(json_path)#切换到任务路径
    wirte_config = open(json_name, "w")
    json.dump(json_dict, wirte_config)
    wirte_config.close()
    os.chdir(old_path)#回到原来的目录
    return '信息更新成功'
######################################################
user_name=getpass.getuser()#获取当前用户名Get the username
print("当前电脑用户名是："+user_name)
os.chdir("c:/printer/received")#把当前目录切换到/printer/received下
print("当前工作目录是"+os.getcwd())
config=get_json('../','config.json')#从config.json文件读取配置信息
print(config)#显示当前的配置信息
serial_number=config['serial_number']#获取任务序号
while (True):
    received_file_list = os.listdir("./")  # 持续地获取传输文件夹的文件列表
    print("当前收到的文件有：\n", received_file_list)
    for task in received_file_list:
        regist_user = re.match('^1[0-9]{10}', task)  # 判断文件夹是否符合命名规则
        user_file_list = os.listdir(task)
        if regist_user and ('info.json' in user_file_list):
            task_abspath = os.path.abspath(task)
            info = get_json(task_abspath, 'info.json')  # 获取info信息
            status = info['user']['status']
            if status == 'received':  # 判断文件是否传输完毕
                print(task + "的所有文件已经传输完毕，开始打印")
                printer.print_files(task_abspath + '/')  # 打印task目录下的文档，只需向printer函数提交一个绝对路径就可以打印该目录所有的文档
                message='用户'+task+'已经打印'
                win32api.MessageBox(0,message,'提示信息',1)
                info['user']['status'] = 'printing'  # 把处理状态修改为printing
                print('当前目录为：', os.getcwd())
                change_json(task_abspath, 'info.json', info)  # 写入info信息，修改status的状态
            elif status == 'receiving':
                print("用户:%s的文件尚未传输完毕，暂不打印" % task)
            elif status == 'printed':
                print("用户:%s的文件打印完毕，无需处理" % task)
            elif status == 'printing':
                print("用户:%s的文件正在打印，无需处理" % task)
    time.sleep(2)#两秒扫描一次文件目录

'''received_file_list=os.listdir("./")#获取传输文件夹的文件列表
print("当前收到的文件有：\n",received_file_list)
#开始提交任务
for task in received_file_list:
    regist_user = re.match('^1[0-9]{10}', task)#判断文件夹是否符合命名规则
    user_file_list = os.listdir(task)
    if regist_user and ('info.json' in user_file_list):
        task_abspath = os.path.abspath(task)
        info = get_json(task_abspath,'info.json') # 获取info信息
        status=info['user']['status']
        if  status=='received':#判断文件是否传输完毕
            print(task+"的所有文件已经传输完毕，开始打印")
            printer.print_files(task_abspath+'/')#打印task目录下的文档，只需向printer函数提交一个绝对路径就可以打印该目录所有的文档
            info['user']['status']='printing'#把处理状态修改为printing
            print('当前目录为：',os.getcwd())
            change_json(task_abspath,'info.json',info)#写入info信息，修改status的状态
        elif status=='receiving':
            print("用户:%s的文件尚未传输完毕，暂不打印"%task)
        elif status=='printed':
            print("用户:%s的文件打印完毕，无需处理"%task)
        elif status=='printing':
            print("用户:%s的文件正在打印，无需处理" % task)'''

improvement="目前BUG：" \
    "1.如果传入多个文件，中间可能夹带其他打印机的任务"