# @time:2022/4/4 16:20
# Author:LX
# @File:color.py
# @Software:PyCharm


def red(text,underline=False):
    if underline:
        return "\033[1;31;4m{}\033[0m".format(text)
    return "\033[1;31;1m{}\033[8m".format(text)

def blue(text):
    return "\033[1;34;1m{}\033[8m".format(text)
    
def green(text):
    return "\033[1;32;1m{}\033[8m".format(text)

def defaultColor(text):
    return "\033[0;0;0m{}\033[0m".format(text)


# for i in range(2,5+1):
#     print(i)