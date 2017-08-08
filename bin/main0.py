#两个文件夹
import getpass
import json
import os
from source import printer
import re
import shutil
def get_config():
    read_config = open("config.json", 'r')
    config = json.load(read_config)
    read_config.close()
    return config
def change_config(config):
    wirte_config = open("config.json", "w")
    json.dump(config, wirte_config)
    wirte_config.close()
user_name=getpass.getuser()#获取当前用户名Get the username
print("当前电脑用户名是："+user_name)
os.chdir("c:/printer")#把当前目录切换到/printer
print("当前工作目录是"+os.getcwd())
config=get_config()#从config.json文件读取配置信息
serial_number=config['serial_number']#获取任务序号
received_file_list=os.listdir("./received")#获取传输文件夹的文件列表
print("当前收到的文件有：\n",received_file_list)
#遍历文件列表，将文件移动到printing文件夹
for task in received_file_list:
    unknown_user = re.search(r'.pdf', task, re.I) #文件名匹配
    regist_user = re.match('^1[0-9]{10}', task)
    if unknown_user: #处理未知用户的任务
        serial_number += 1
        config["serial_number"]=serial_number
        change_config(config)# 向json文件写入任务序号
        print("创建第"+str(serial_number)+"个任务")
        os.mkdir("./printing/"+str(serial_number)+"_unknown/")
        shutil.move("./received/"+task,"./printing/unknown_"+str(serial_number)+"/"+task)
    elif regist_user:#处理已知账号用户的任务（优化任务，最后复制info.json文件，保证复制完成之后才开始打印操作）
        user_file_list=os.listdir("./received/"+task)
        if "info.json" in user_file_list:#判断info.json文件（包含了文档打印信息，最后传输）是否存在用于判断文件是否传输完毕
            serial_number += 1#任务序列号加1
            config['serial_number'] = serial_number
            change_config(config)#写入config.json记录任务序列号
            print("创建第"+str(serial_number)+"个任务")
            os.rename("./received/" + task,"./received/"+str(serial_number)+"_"+task)
            shutil.move("./received/"+str(serial_number)+"_"+task,"./printing/")
        else:
            print("用户:%s的文件尚未传输完毕，暂不打印"%task)
print('正在传输的文件还有%s:'%os.listdir('./received'))
printer.print_files(r'c:/printer/received/1_18796282979/')#打印测试文件夹中的文件

improvement="目前BUG：" \
    "1.如果传入多个文件，中间可能夹带其他打印机的任务"