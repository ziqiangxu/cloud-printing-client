from urllib.request import urlopen
import re
import json
SITE = "http://yixiu.life:8000"
LOCAL_PATH = "/printer/rec"

def get_task():
    tel = '18796282979'
    path_url = "%s/get_task/?tel=%s" % (SITE, tel)
    result = urlopen(path_url)
    result_str = str(result.read())
    task_path = result_str[2:-1].split("*")
    print(task_path)
    return task_path


def get_info():
    for path in get_task():
        fragment = path.split("/")
        tel = fragment[-3]
        task_ID = fragment[-2]
        files = fragment[-1].split(",")
    with open("%s")
        #info = info.read().split("/")(-3)
        #with open("/printer/received/%s/%s/info.json" % , "wb") as f:
         #   f.write(info.read())

get_info()
