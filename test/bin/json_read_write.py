"""
读写json文件：
读：传入json文件的路径和一个字典名，并把内容存在字典里，返回bool值
写：传入json文件路径和一个字典，向json文件写入字典内容，返回bool值
"""
import os
import json


def read(path):
    try:
        f = open(path, 'r')
        content = json.load(f)
        f.close()
        return content
    except:
        return False


def write(path, dict_):
    try:
        f = open(path, "w")
        json.dump(dict_, f)
        f.close()
        return True
    except:
        return False
