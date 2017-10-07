from urllib.request import urlopen
import os
SITE = "http://yixiu.life:8000"
LOCAL_PATH = "\\printer\\received"
WHERE = "receiver3"


def get_task():
    tel = '18796282979'
    path_url = "%s/get_task/?tel=%s" % (SITE, tel)
    result = urlopen(path_url)
    result_str = str(result.read())
    task_path = result_str[2:-1].split("*")
    print(task_path)
    return task_path


def file_url(tel, task_ID):
    url =SITE + "/download/?path=/home/cloud_printing/received_files/%s/%s" % (tel, task_ID)
    return url


def get_files():
    for path in get_task():
        fragment = path.split("/")
        tel = fragment[-3]
        task_ID = fragment[-2]
        files = fragment[-1].split(",")
        task_path = os.path.join(LOCAL_PATH, tel, task_ID)
        # os.makedirs(task_path, 0o777, True)
        try:
            os.makedirs(task_path)
        except:
            print(WHERE, "文件夹已存在，创建任务路径失败")
        for file in files:
            url = file_url(tel, task_ID) + "/" + file
            print(url)
            try:
                with open(os.path.join(task_path, file), "wb") as f:
                    try:
                        file_stream = urlopen(url)
                    except:
                        print(WHERE, "从服务器获取文件失败")
                    f.write(file_stream.read())
                    # 给服务器发送消息，修改任务状态

            except:
                print(WHERE, "保存文件失败")

get_files()
