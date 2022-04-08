# -*- coding:utf-8 -*-
# @time:2022/4/4 10:08
# Author:LX
# @File:log.py
# @Software:PyCharm
'''
    # 日志类
'''

from header import (
    os,
    datetime,
)


# 日志类
class Log(object):
    def __init__(self,is_log=False,log_path=None):
        # 记录所的path 结构[(时间,定位方式,路径,备注)]
        self.__record_path = []
        self.__is_log = False
        self.__log_path = "recordPath.log"
        if is_log:
            self.setEnableLog(is_log)
        if log_path:
            self.setLogPath(log_path)

    # 设置日志是否启用
    def setEnableLog(self,b_log):
        self.__is_log = b_log

    # 获取日志的启用状态
    def state(self):
        return self.__is_log

    # 设置日志存放路径
    def setLogPath(self, path="."):
        self.__log_path = path

    # 返回日志路径
    def logPath(self):
        return self.__log_path

    # 添加日志信息(外部不需要调用)
    def addLogInfo(self,info):
        self.__record_path.append(info)

    # 在本地生成日志
    def log(self,path="",connector=":"):
        if not path:
            path = self.logPath()
        # 生成日志
        if not os.path.isfile(path):
            open(path, "w").close()
        with open(path, "a") as f:
            currentTime = datetime.datetime.now().strftime('%Y@%m@%d %H@%M@%S'.replace("@", connector))
            f.write("============{}============\n".format(currentTime))
            for info in self.__record_path:
                data = '''
path_type:{}
path:{}
time:{}
note:{}
                '''.format(info[1], info[2], info[0], info[3])
                f.write(data)
            f.write("\n============end============\n")