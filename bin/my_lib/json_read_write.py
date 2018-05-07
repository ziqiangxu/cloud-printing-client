"""
读写json文件：
读：传入json文件的路径和一个字典名，并把内容存在字典里，返回bool值
写：传入json文件路径和一个字典，向json文件写入字典内容，返回bool值
"""
import os
import json


def read(path):
    try:
        print(path)
        f = open(path, 'r')
        content = dict(json.load(f))
        f.close()
        return content
    except FileNotFoundError:
        print(__file__, "Can't find the file")
        return {}
    except:
        return {}


def write(path, dict_):
    try:
        f = open(path, "w")
        json.dump(dict_, f)
        f.close()
        return True
    except:
        return False
