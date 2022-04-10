# -*- coding:utf-8 -*-
# @time:2022/4/4 9:53
# Author:LX
# @File:header.py
# @Software:PyCharm
'''

    公共头文件
    排序规律: 由短到长

'''
import re
import os
import subprocess
import sys
import time
import json
import math
import random
import datetime
import pyautogui
import traceback
import win32com.client
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
# os.system("chrome.exe")
# os.popen(cmd)
# subprocess.Popen(cmd)
# ----------------------------------------------------------------

# 移动系列
# dm.MoveTo(100,100)
# print dm.GetCursorShape()

# 鼠标系列
# dm.LeftClick()
# dm.RightClick()
# dm.LeftDoubleClick()
# dm.MiddleClick()

# 键盘系统
# dm.KeyDown()
# dm.KeyUp()
# dm.KeyPress() # 传虚拟码
# dm.KeyPressChar('a')

# ctrl+a
# dm.KeyDownChar('ctrl')
# dm.KeyPressChar('a')
# dm.KeyUpChar('ctrl')

# dm.KeyPressStr("hello",3)

# 获取鼠标在屏幕的位置
# print dm.GetCursorPos(0,0)

# print dm.GetMousePointWindow()

# 截图
# dm.Capture(0,0,300,300,"xx.png")

# chromeOptions = webdriver.ChromeOptions()
#
# chromeOptions.add_argument('--lang=en-US')
# chromeOptions.add_argument("--test-type")
# chromeOptions.add_argument("--ignore-certificate-errors")
# chromeOptions.add_argument('--proxy-server=socks5://localhost:5000')
# chromeOptions.add_argument('--remote-debugging-port=9222')
# chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
