# -*- coding: utf-8 -*-
# @time:2022/3/26 9:31
# Author:lx
# @File:personificationAuto.py
# @Software:PyCharm

'''

    拟人自动化操作库
    接管：
   终端执行 chrome.exe --remote-debugging-port=9222 --user-data-dir="D:\code\my_python\PersonificationAuto\test_selenium"
   options参数配置下面
   op = {
    # "add_experimental_option":[("debuggerAddress","127.0.0.1:9222")]
}
'''
from __future__ import print_function

import os.path

from header import (
    sys,
    time,
    math,
    random,
    datetime,
    win32com,
    pyautogui,
    webdriver,
)
from log import Log
from elementPosition import ElementPosition
from color import PrintColor

# 拟人化操作类
class PersonificationAuto(object):
    '''
        该类没有直接操作多个元素对象的方法,

    '''
    # 1递增，2递减
    INCREASING = 1
    DIMINISHING = 2

    def __init__(self,driver=None,executable_path="chromedriver.exe",options=None,age=None,is_log=False,log_path=None,is_tracking_path=False,
                 start_time=0.0,end_time=0.0):
        '''

        :param executable_path: 驱动路径
        :param options: 配置列表
            {"add_argument":[],
            “add_experimental_option”：[(xx,xx),xx,...]}
        :param age:操作人的年龄范围
        :param is_log: 是否生成日志
        :param log_path: 日志路径
        :param is_tracking_path: 行动轨迹
        :param start_time:随机等待的开始时间
        :param end_time: 随机等待的结束时间
        '''
        # 创建驱动对象
        # 处理网页的显示通知(默认处理)
        prefs = {
            'profile.default_content_setting_values': {
                'notifications': 2
            }
        }
        if driver:  # 接收外部驱动
            self.__driver = driver
        elif options:
            self.__chromeOptions = webdriver.ChromeOptions()
            # self.__chromeOptions.add_experimental_option('prefs', prefs)
            for k,v in options.items():
                for value in v:
                    if k == "add_argument":
                        self.__chromeOptions.add_argument(value)
                    if k == "add_experimental_option" and isinstance(value,tuple):
                        self.__chromeOptions.add_experimental_option(*value)
            self.__driver = webdriver.Chrome(executable_path=executable_path,options=self.__chromeOptions)
        else:
            options = webdriver.ChromeOptions()
            options.add_experimental_option('prefs', prefs)
            self.__driver = webdriver.Chrome(executable_path=executable_path)
        # 创建元素位置类
        # self.__ele_position = ElementPosition(driver=self.__driver)
        # 维护的元素对象
        self.__per_ele = []
        # 行踪列表 格式: [{'time';'xxx','fname':'xxx','data':'xxxx'}]
        self.__tracking_path_list = list()
        # 是否显示记录
        self.__tracking_path = is_tracking_path
        # 年龄
        if not age:
            self.__age = age
        else:
            self.__age = 18
        # 默认鼠标移动速度
        self.__mouse_speed = [0.1,0.2]
        # 大漠
        self.__dm = win32com.client.Dispatch('dm.dmsoft')
        # 随机等待随机
        self.__start_time, self.__end_time = start_time,end_time
        # 浏览器窗口索引
        self.__win_handles_index = 0
        # 日志对象
        self.__log_obj = Log(is_log,log_path)
        # 记录所的path 结构[(时间,定位方式,路径,备注)]
        # self.__record_path = []
        # 错误信息的最大递归深度
        if hasattr(sys, 'tracebacklimit'):
            self.__max_limit = sys.tracebacklimit
        else:
            self.__max_limit = None
        # 记录输入sendkeys的值,用于对比
        self._old_sendkeys_value = None


    def lookOptionList(self):
        '''
        查看options配置信息
        :return:
        '''
        temp = [
            "--lang=en-US",
            "--test-type",
            "-ignore-certificate-errors",
        ]
        for info in temp:
            print(info)

    # 设置显示错误的最大深度
    def setErrorLimit(self,limit=None):
        '''
            不设置默认递归到最大深度
        :param limit: 类型int
        :return:
        '''
        if self.__tracking_path:
            self.__max_limit = limit

    def setAge(self,age=15):
        '''
            设置操作人的年龄,年龄决定鼠标移动的速度
        :param age:  当前年龄
        :return: 
        '''
        if  age >= 10 and age <= 15 or 36 <= age and age <= 59:
            self.setMouseSpeed(0.7, 0.9)
        elif age >= 16 and age <= 35:
            self.setMouseSpeed(0.8, 1)
        elif age >= 60 and age <= 80:
            self.setMouseSpeed(1.5, 2)
        else:
            self.setMouseSpeed(1.5, 2.5)
        self.__age = age

    # 设置鼠标移动速度
    def setMouseSpeed(self,min_speed,max_speed):
        '''
            设置鼠标移动速度
        '''
        self.__mouse_speed = [min_speed,max_speed]

    def age(self):
        return self.__age

    # 获取日志对象
    def getLogObj(self):
        return self.__log_obj

    # 获取鼠标移动速度
    def mouseSpeed(self):
        return self.__mouse_speed

    # 获取当前元素个数
    def elementNumber(self):
        if isinstance(self.element(), list):
            return len(self.element())
        return 1

    # 获取操作者的鼠标移动速度
    def __getRaodomMuseSpeed(self):
        return round(random.uniform(*self.mouseSpeed()),1)

    # 添加跟踪路径
    def __addRackingRath(self,_time,fname,data):
        temp = {'time':_time,
                'fname':fname,
                'data':data}
        self.__tracking_path_list.append(temp.copy())

    # 显示最近的跟踪记录
    def __showCurrentRacking(self,is_func_err=False):
        if self.__tracking_path_list:
            _time = self.__tracking_path_list[-1]['time']
            fname = self.__tracking_path_list[-1]['fname']
            data = self.__tracking_path_list[-1]['data']
            if data is None:
                print(PrintColor.defaultColor('----- [{}]'.format(_time)),end="")
                # print(defaultColor('----- [{}]').format(_time),end="")
                PrintColor.printCColor(is_func_err,
                                       ' <{}>'.format(fname),
                                       ('red','green'))
                # if is_func_err:
                #     print(PrintColor.red(' <{}>').format(fname))
                # else:
                #     print(PrintColor.green(' <{}>').format(fname))
            elif isinstance(data,int) \
                    or isinstance(data,str) \
                    or isinstance(data,list) \
                    or isinstance(data,tuple) \
                    or (data[0] != 0 and data[1] != 0):
                print(PrintColor.defaultColor('----- [{}]').format(_time), end="")
                PrintColor.printCColor(is_func_err,
                                       ' <{}>'.format(fname),
                                       ('red', 'green'),end="")
                PrintColor.printColor(
                    [
                        (' argv: ','defaultColor'),
                        ('{}'.format(data),"blue")
                    ])
                # if is_func_err:
                #     print(red(' <{}>').format(fname),end="")
                # else:
                #     print(green(' <{}>').format(fname),end="")
                # print(defaultColor(' argv: '),end="")
                # print(blue('{}').format(data))

    def __isRacking(self):
        return self.__tracking_path

    def maxWin(self):
        self.__addRackingRath(self.currentTime(),
                              "maxWin",
                              None)
        if self.__isRacking():
            self.__showCurrentRacking()
        self.__driver.maximize_window()
        return self

    def minWin(self):
        self.__addRackingRath(self.currentTime(),
                              "minWin",
                              None)
        if self.__isRacking():
            self.__showCurrentRacking()
        self.__driver.minimize_window()
        return self

    def currentTime(self, connector_before=":", connector_after=":",custom=None):
        '''
        返回当前时间
        Return current time
        :connector_before: 年月日之间连接符
        :connector_after:时分秒之间连接符
        :custom:自定义
        :return: str
        '''
        _time = '%Y@1%m@1%d %H@%M@%S'.replace("@1",connector_before)
        _time = _time.replace("@",connector_after)
        if custom:
            _time = custom
        return datetime.datetime.now().strftime(_time)

    def element(self):
        '''
            如果单个元素,则类型是ElementPosition
            如果是多个元素,则类型是list
        :return:
        '''

        return self.__per_ele

    def driver(self):
        return self.__driver

    def setElement(self,ele):
        if isinstance(ele,list):
            if len(ele) == 1:
                self.__per_ele = ElementPosition(self.__driver, ele[0])
                return self
            # 多个元素拆解在包装
            self.__per_ele = []
            for e in ele:
                self.__per_ele.append(ElementPosition(self.__driver,e))
        else:
            self.__per_ele = ElementPosition(self.__driver,ele)
        return self

    def get(self,url):
        # platform.platform()
        if url[0] == "/":  # 针对Mac系统打开本地文件
            url = "file://"+url
        self.__driver.get(url)
        self.__addRackingRath(self.currentTime(),
                            "get",
                            url)
        if self.__isRacking():
            self.__showCurrentRacking()
        return self

    # 日志
    def log(self,path="",connector=":"):
       self.__log_obj.log(path,connector)

    def __compare(self,data1, data2):
        '''
                比较data1中的数据是否在data2中
        :param data1:
        :param data2:
        :return:
        '''
        for i in data1:
            if i in data2:
                return True
        return False

    # 模板
    def __findTemplate(self, path_type, path, start_time, end_time,note,is_stop):
        if self.getLogObj().state():
            self.__log_obj.addLogInfo((self.currentTime(),path_type,path,note)) # 记录所有的路径
        self.__wait(start_time, end_time)
        # 默认匹配多个元素
        if isinstance(path,list):
            e = None
            for path_e in path:
                try:
                    e = self.__driver.find_elements(path_type, path_e)
                    if e:
                        self.setElement(e)
                        break
                    else:
                        e = None
                except:
                    e = None
                self.__wait(start_time, end_time)
            else:
                if e is None:
                    raise TypeError("No elements were matched,{}\n".format(path))
        else:
            e = self.__driver.find_elements(path_type, path)
            if e:
                self.setElement(e)
            else:
                raise TypeError("No elements were matched,\"{}\"\n".format(path))

    #  递归显示代码错误
    def __errorDisplay(self,err_bool,receive_err,is_stop=True):
        if is_stop and self.__isRacking():
            self.__showCurrentRacking(is_func_err=err_bool)
            exc_type, exc_value, exc_traceback_obj = sys.exc_info()
            limit = self.__max_limit
            n = 0
            while exc_traceback_obj is not None and (limit is None or n < limit):
                lineno = exc_traceback_obj.tb_lineno
                co = exc_traceback_obj.tb_frame.f_code
                filename = co.co_filename
                name = co.co_name
                # 这句话格式可以实现报错后,在pycharm中点击跳转
                print(PrintColor.red('  File "%s", line %d, in <%s>'% (filename, lineno, name)))
                exc_traceback_obj = exc_traceback_obj.tb_next
                n += 1
            if receive_err:  # 显示具体报错信息
                print(receive_err, end="")

    # 模板2 - 匹配规则的模板
    def __errorFrameMatch(self,func_str_name,path,start_time, end_time,note,is_stop):
        err_bool = False
        receive_err = None  # 接收错误信息
        try:
            if is_stop:
                self.__addRackingRath(self.currentTime(),
                                      func_str_name,
                                      path)

            self.__findTemplate(func_str_name, path, start_time, end_time, note,is_stop=is_stop)
            if is_stop and self.__isRacking():
                self.__showCurrentRacking()
        except Exception as e:
            err_bool = True
            receive_err = e
        finally:
            self.__errorDisplay(err_bool,receive_err,is_stop= True if err_bool else False)
            
    # 自动匹配
    def autoMatch(self,paths_type,paths):
        '''
            多个匹配方式对应多条路径(比较耗时)
            xx.autoMatch(["id","xpath"],["xxx","xxxx"])
            多对一
            多对多
            一对多
        :param path: 元素的匹配路径
        :return:
        '''
        err_bool = False
        receive_err = None  # 接收错误信息
        # 调用函数列表
        functools = {
            "id":self.id,
            "xpath":self.xpath,
            "css":self.css,
            "class name":self.className,
            "css selector":self.cssSelector,
            "link text":self.linkText,
            "partial link text":self.linkTextPartial
        }
        self.__addRackingRath(self.currentTime(),
                              "autoMatch",
                              (paths_type,paths))
        # 如果该参数是str,则把它变成长度为1的列表
        if isinstance(paths_type,str):
            paths_type = [paths_type]


        for type_ in paths_type:
            functools[type_](paths, is_stop=False)
        #     try:
        #         functools[type_](paths,is_stop=False)
        #     except Exception as e:
        #         err_bool = True
        #         receive_err = e
        # print("=============",receive_err)
        # if self.__isRacking():
        #     self.__showCurrentRacking()
        return self

    def id(self,path,start_time=None,end_time=None,note="",is_stop=True):
        self.__errorFrameMatch("id", path, start_time, end_time, note,is_stop)
        return self

    def xpath(self,path,start_time=None,end_time=None,note="",is_stop=True):
        self.__errorFrameMatch("xpath",path,start_time, end_time,note,is_stop)
        return self

    def css(self,path,start_time=None,end_time=None,note="",is_stop=True):
        self.__errorFrameMatch("css", path, start_time, end_time, note,is_stop)
        return self

    def tagName(self,path,start_time=None,end_time=None,note="",is_stop=True):
        self.__errorFrameMatch("tag name", path, start_time, end_time, note,is_stop)
        return self

    def className(self,path,start_time=None,end_time=None,note="",is_stop=True):
        self.__errorFrameMatch("class name", path, start_time, end_time, note,is_stop)
        return self

    def cssSelector(self,path,start_time=None,end_time=None,note="",is_stop=True):
        self.__errorFrameMatch("css selector", path, start_time, end_time, note,is_stop)
        return self

    def linkText(self,path,start_time=None,end_time=None,note="",is_stop=True):
        self.__errorFrameMatch("link text", path, start_time, end_time, note,is_stop)
        return self

    def linkTextPartial(self,path,start_time=None,end_time=None,note="",is_stop=True):
        self.__errorFrameMatch("partial link text", path, start_time, end_time, note,is_stop)
        return self

    def __input(self,str_data,trend_mode=1,trend_speed=0.2):
        speed = trend_speed
        for c in str_data:
            # self.__dm.KeyPressChar(c)
            pyautogui.press(c)
            # 每次输入都是随机间隔,实现快慢打字
            if trend_mode == PersonificationAuto.INCREASING:
                time.sleep(self.__getRaodomMuseSpeed() / random.uniform(1.0,
                                                                      3.0 - speed))
            if trend_mode == PersonificationAuto.DIMINISHING:
                time.sleep(self.__getRaodomMuseSpeed() / random.uniform(1.0,
                                                                      3.0 + speed))
            if trend_mode == PersonificationAuto.INCREASING | PersonificationAuto.DIMINISHING:
                time.sleep(self.__getRaodomMuseSpeed() / random.uniform(1.0,3.0))

    def moveTo(self,x=None,y=None,_time=None,is_stop=True):
        '''
            如果不传值,可以自动计算位置,移动的时间可以跟随年龄而变化
        :param x: 
        :param y:
        :param _time:
        :param is_stop:暂时不用这个参数
        :return:
        '''
        if not x and not y:
            err_bool = False  # 如果这个变量变成True,那么这个方法报错
            receive_err = None  # 接收错误信息
            try: # 检测元素是否能正常使用
                x = self.element().x()
                y = self.element().y()
                if is_stop and self.__isRacking():
                    self.__addRackingRath(self.currentTime(),
                                          "moveTo",
                                          (x, y))
                    self.__showCurrentRacking()
            except Exception as e:
                err_bool = True
                receive_err = str(e)+",element() currently return a list, not an ElementPosition object.\n"
                self.__addRackingRath(self.currentTime(),
                                      "moveTo",
                                      (x, y))
            finally:
                self.__errorDisplay(err_bool, receive_err,is_stop= True if err_bool else False)
        else:
            self.__addRackingRath(self.currentTime(),
                                  "moveTo",
                                  (x, y))
            if is_stop and self.__isRacking():
                self.__showCurrentRacking()
        if not _time:
            _time = self.__getRaodomMuseSpeed()
        pyautogui.moveTo(x,y,_time)
        return self

    def send_keys(self,str_data,trend_mode=1,trend_speed=0.2,is_click=True,is_clear=False,is_verify=True,is_stop=False):
        '''
            输入数据
        :param str_data: 输入的数据
        :param trend_mode: 输入数据的模式 递增：1 递减: 2 匀速: 3
        :param trend_speed: 影响递增，递减的数值(小数)
        :param is_click: 输入前是否点击
        :param is_clear: 输入前是否先清空原本的数据
        :param is_verify:是否验证数据是真的输入了
        :return:
        '''
        self.moveTo(is_stop=True)
        if is_click or is_clear:
            self.click(is_stop=True)
            # self.__dm.LeftClick()
        if is_clear:
            # self.__dm.KeyDownChar('ctrl')
            # self.__dm.KeyDownChar('a')
            # self.__dm.KeyPressChar('x')
            # self.__dm.KeyUpChar('ctrl')
            pyautogui.keyDown('ctrl')
            pyautogui.press('a')
            pyautogui.press('x')
            pyautogui.keyUp('ctrl')
        # 输入
        self.__input(str_data,trend_mode,trend_speed)
        # if is_stop:
        if is_verify:
            self._old_sendkeys_value = self.element().value
            self.__addRackingRath(self.currentTime(),
                                  "send_keys",
                                  self._old_sendkeys_value)
        else:
            new_value = self.element().value
            data = self._old_sendkeys_value + " != " + new_value
            # 新输入的数据和传入的数据再次比较
            if new_value == str_data:
                data += " [yes]"
            else:
                data += " [no] raw=%s"%str_data
            self.__addRackingRath(self.currentTime(),
                                  "send_keys",
                                  data)
        if not is_stop and self.__isRacking():
            self.__showCurrentRacking()
        if is_verify:
             if str_data != self.element().value:
                 time.sleep(random.randint(2,3))
                 self.send_keys(str_data,trend_mode,trend_speed,is_click,is_clear=True,is_verify=False)
        return self

    def __click(self,click_f,number=1,func_name="",start_time=0.2,end_time=0.4,is_move=True,is_stop=True):
        # 添加追踪日志
        if is_stop:
            self.__addRackingRath(self.currentTime(),
                                  func_name,
                                  None)
        if is_move:
            self.moveTo(is_stop=False)
        if number > 1:
            for _ in range(number):
                # self.__dm.LeftClick()
                self.click(is_stop=False)
                self.wait(start_time, end_time, is_stop=False)
            return
        click_f()
        if is_stop and self.__isRacking():
            self.__showCurrentRacking()

    def click(self,number=1,start_time=0.2,end_time=0.4,is_move=True,is_stop=True):
        '''

        :param number: 点击的次数
        :param start_time:
        :param end_time:
        :param is_move: 点击前是否先移动
        :return:
        '''
        # self.__click(self.__dm.LeftClick,number,"click",start_time,end_time,is_move,is_stop)
        self.__click(pyautogui.click,number,"click",start_time,end_time,is_move,is_stop)
        return self

    def rightClick(self,number=1,start_time=0.2,end_time=0.4,is_move=True,is_stop=True):
        # self.__click(self.__dm.RightClick, number,"rightClick", start_time, end_time,is_move,is_stop)
        self.__click(pyautogui.rightClick, number,"rightClick", start_time, end_time,is_move,is_stop)
        return self


    def LeftDoubleClick(self,number=1,start_time=0.2,end_time=0.4,is_move=True,is_stop=True):
        # self.__click(self.__dm.LeftDoubleClick, number,"LeftDoubleClick" ,start_time, end_time,is_move,is_stop)
        self.__click(pyautogui.doubleClick, number,"LeftDoubleClick" ,start_time, end_time,is_move,is_stop)
        return self

    # 回车
    def enter(self,start_time=0.0,end_time=0.0,is_stop=True):
        if is_stop:
            self.__addRackingRath(self.currentTime(),
                                  "enter",
                                  None)
            if self.__isRacking():
                self.__showCurrentRacking()
        self.wait(start_time, end_time,is_stop=True)
        self.__dm.KeyDownChar("enter")
        self.__dm.KeyUpChar("enter")
        return self

    def tab(self,start_time=0.0,end_time=0.0):
        self.__addRackingRath(self.currentTime(),
                              "tab",
                              None)
        if self.__isRacking():
            self.__showCurrentRacking()
        self.wait(start_time, end_time,is_stop=True)
        self.__dm.KeyDownChar("tab")
        self.__dm.KeyUpChar("tab")
        return self

    def scroll(self, value=40,start_time=2, end_time=2,direction="bottom"):
        # scroll_js = "document.documentElement.scrollTop={}".format(value)
        # self.__driver.execute_script(scroll_js)
        # 每秒多少段
        _time = random.randint(start_time,end_time)
        period = value//_time
        for _ in range(_time):
            if direction == "bottom":  # 下
                pyautogui.scroll(-period)
            elif direction == "top": # 上
                pyautogui.scroll(period)
            elif direction == "right": # 右
                pyautogui.hscroll(period)
            elif direction == "left": # 左
                pyautogui.hscroll(-period)
            self.wait(1,1)
        return self

    # 滚动条到底端
    def scrollBottom(self,start_time=1, end_time=1):
        self.scroll(1200,start_time,end_time,"bottom")
        return self

    # 滚动条到顶端
    def scrollTop(self,start_time=1, end_time=1):
        self.scroll(0, start_time,end_time, "top")
        return self

    # 滚动条向左移动
    # def scrollLeft(self, value):
    #     js = "window.scrollTo(0,{})".format(value)
    #     self.__driver.execute_script(js)
    #     return self

    # 滚动条向右移动
    # def scrollRightValue(self, value):
    #     js = "window.scrollTo({},0)".format(value)
    #     self.__driver.execute_script(js)
    #     return self

    # 滚动条向左移动
    def scrollLeft(self,start_time=1, end_time=1):
        self.scroll(0, start_time,end_time, "left")
        return self

    # 滚动条向右移动
    def scrollRight(self,start_time=1, end_time=1):
        self.scroll(1200, start_time,end_time, "right")
        return self

    # 等待时间
    def wait(self,start_time=None,end_time=None,is_stop=True):
        if is_stop:
            self.__addRackingRath(self.currentTime(),
                                  "wait",
                                  (start_time,end_time))
            if self.__isRacking():
                self.__showCurrentRacking()
        if not start_time or not end_time:
            start_time,end_time = self.__start_time,self.__end_time
        time.sleep(random.uniform(start_time,end_time))
        return self

    def __wait(self,start_time=None,end_time=None,is_stop=False):
        if not start_time or not end_time:
            self.wait(self.__start_time, self.__end_time,is_stop)
        else:
            self.wait(start_time, end_time)

    # 退出浏览器
    def quit(self,start_time=None,end_time=None):
        self.__addRackingRath(self.currentTime(),
                              "quit",
                              None)
        self.__wait(start_time, end_time,is_stop=False)
        self.__driver.quit()
    
    def newElement(self,path_type,path):
        return ElementPosition(self.__driver,self.__driver.find_element(path_type,path))

    def drag(self,x1,y1,x2,y2):
        '''
            鼠标在坐标(x1,y2)出按下,(x2,y2)松开
        :param x1:
        :param y1:
        :param x2:
        :param y2:
        :return:
        '''
        self.__addRackingRath(self.currentTime(),
                              "drag",
                              [(x1,y1),(x2,y2)])
        if self.__isRacking():
            self.__showCurrentRacking()
        self.moveTo(x1,y1)
        pyautogui.mouseDown()
        self.moveTo(x2,y2)
        pyautogui.mouseUp()
        return self

    def dragTo(self,x,y):
        '''
            将元素拖拽到某个坐标
        :param x:
        :param y:
        :return:
        '''
        self.__addRackingRath(self.currentTime(),
                              "dragTo",
                              (x,y))
        if self.__isRacking():
            self.__showCurrentRacking()
        self.moveTo()
        pyautogui.mouseDown()
        self.moveTo(x,y)
        pyautogui.mouseUp()
        return self

    # 鼠标拖拽元素
    def dragToDrop(self,newEle):
        '''

        :param newEle: 放置目标的元素对象(请使用newElement方法去创建对象)
        :return:
        '''
        self.__addRackingRath(self.currentTime(),
                              "dragToDrop",
                              newEle.shape)
        if self.__isRacking():
            self.__showCurrentRacking()
        self.moveTo()
        pyautogui.mouseDown()
        self.setElement(newEle)
        self.moveTo()
        pyautogui.mouseUp()
        return self

    def frame(self):
        '''
            进入内嵌框架(进文档)
        '''
        self.__addRackingRath(self.currentTime(),
                              "frame",
                              None)
        if self.__isRacking():
            self.__showCurrentRacking()
        self.__driver.switch_to.frame(self.element())
        return self

    def defaultContent(self):
        '''
            切换到默认文档
        :return:
        '''
        self.__addRackingRath(self.currentTime(),
                              "defaultContent",
                              None)
        if self.__isRacking():
            self.__showCurrentRacking()

        self.__driver.switch_to.default_content()
        return self

    def goWin(self, index=0,stop=False):
        '''
            切换到指定浏览器窗口
        :param index:
        :param index: 阻止其他函数调用此函数打印多余的信息
        :return:
        '''

        win_handles = self.__driver.window_handles
        self.__driver.switch_to.window(win_handles[index])
        if not stop:
            self.__addRackingRath(self.currentTime(),
                                  "goWin",
                                  index)
            if self.__isRacking():
                self.__showCurrentRacking()
        return self

    def nextWin(self):
        '''
            切换到到浏览器下一个窗口
        '''
        win_handles = self.__driver.window_handles
        win_handles_len = len(win_handles)
        current_win = self.__driver.current_window_handle
        index = win_handles.index(current_win)
        index += 1
        if index < win_handles_len:
            self.goWin(index,stop=True)
            self.__addRackingRath(self.currentTime(),
                                  "nextWin",
                                  index)
            if self.__isRacking():
                self.__showCurrentRacking()

        return self

    def onWin(self):
        '''
             切换到到浏览器上一个窗口
        '''
        win_handles = self.__driver.window_handles
        current_win = self.__driver.current_window_handle
        index = win_handles.index(current_win)
        index -= 1
        if index >= 0:
            self.goWin(index,stop=True)
            self.__addRackingRath(self.currentTime(),
                                  "onWin",
                                  index)
            if self.__isRacking():
                self.__showCurrentRacking()
        return self

    # 刷新浏览器
    def refresh(self):
        self.driver().refresh()
        return self

    # 浏览器前进
    def forward(self):
        self.driver().forward()
        return self

    # 浏览器后退
    def back(self):
        self.driver().back()
        return self

    def closeWin(self):
        '''
            关闭当前浏览器窗口
        :return:
        '''
        self.__driver.close()

    def up(self):
        self.__dm.KeyPress(38)
        return self

    def down(self):
        self.__dm.KeyPress(40)
        return self

    def left(self):
        self.__dm.KeyPress(37)
        return self

    def right(self):
        self.__dm.KeyPress(39)
        return self
    
    def selectOp(self,number=None,direction="ud",scope=None,probability=None,start_time=0.5,end_time=0.9):
        '''

        :param number: 随机选择的次数范围(默认7-10次数)
        :param direction: 选择的方向
                ud: 上下选择
                lr: 左右选择
        :param scope: 选择的范围(默认在所有选项中选择)
        :param probability: 选择选项所分布的概率
        :param start_time: 随机选择间隔的开始时间
        :param end_time: 随机选择间隔的结束时间
        :return:
        '''
        # 获取选择次数
        if number is None:
            number = random.randint(7,10)
        else:
            if isinstance(number,list):
                number = random.randint(*number)

        # 选择方向
        if direction.lower() == "ud":
            exe_f1, exe_f2 = self.down, self.up
        elif direction.lower() == "lr":
            exe_f1, exe_f2 = self.left, self.right

        self.click(is_stop=False)

        # 生成数据分布列表内部函数
        def getSamplingData(s,e,probability):
            temp_list, count = [], 0
            for i in range(s, e + 1):  # 确认选择范围
                temp_list.extend([i for _ in range(1, probability[count] + 1)])  # 生成概率列表
                count += 1
            return temp_list

        # 上下移动-内部函数
        def move(number,data_list,pos_index,exe_f1, exe_f2):
            # 选择方向
            for _ in range(number):
                # 随机挑选一个坐标
                random_index = random.choice(data_list)
                for _ in range(int(math.fabs(pos_index - random_index))):
                    if random_index > pos_index:
                        exe_f1()
                    if random_index < pos_index:
                        exe_f2()
                    time.sleep(random.uniform(start_time, end_time))
                pos_index = random_index  # 更新位置坐标

        length = self.element().length  # 获取select长度
        if not isinstance(self.element(), list):
            pos_index = 0 # 位置坐标

            # 既有分布概率,又有选择范围
            if probability and scope:
                data_list = getSamplingData(scope[0],scope[1]+1,probability)
                # 首先走到范围的首项
                for _ in range(scope[0]):
                    self.down()
                    time.sleep(random.uniform(start_time, end_time))
                pos_index = scope[0]  # 更新位置坐标
                move(number, data_list, pos_index, exe_f1, exe_f2)

            # 只有分布概率
            if probability:
                data_list = getSamplingData(0,length-1,probability)
                move(number, data_list, pos_index,exe_f1, exe_f2)

            # 分布概率,选择范围都没有时
            if probability is None and scope is None:
                scope = [0,length]

            # 只有选择范围
            if scope:
                # 首先走到范围的首项
                for _ in range(scope[0]):
                    self.down()
                    time.sleep(random.uniform(start_time, end_time))
                pos_index = scope[0] # 当前索引位置
                # 生成选择的索引列表
                data_list = [i for i in range(scope[0],scope[1]+1)]
                move(number, data_list, pos_index, exe_f1, exe_f2)

            self.enter(is_stop=False)
            self.__addRackingRath(self.currentTime(),
                                  "selectOp",
                                  None)
            if self.__isRacking():
                self.__showCurrentRacking()
        return self

    # 获取select下拉框元素个数
    def selectGetNumber(self,match_way,value):
        if match_way == "id":
            js = '''
                    return document.getElementById("{}").length
                    '''.format(value)
        elif match_way == "class name":
            js = '''
                    return document.getElementsByClassName("{}")[0].length
                    '''.format(value)
        elif match_way == "tag name":
            js ='''
            return document.getElementsByTagName("{}")[0].length
            '''.format(value)
        else:
            raise TypeError("selectGetNumber not!")

        number = self.__driver.execute_script(js)
        return number

    def selectGetText(self,match_way,value,index):
        if match_way == "id":
            js ='''
                var s = document.getElementById("{}");
                return s[{}].text
            '''.format(value,index)
        elif match_way == "class name":
            js = '''
            var s = document.getElementsByTagName("{}");
            return s[0][{}].text
            '''.format(value,index)
        elif match_way == "tag name":
            js = '''
                var s = document.getElementsByClassName("{}");
                return s[0][{}].text
            '''.format(value,index)
        else:
            raise TypeError("selectGetText not!")
        text = self.__driver.execute_script(js)
        return text

    def selectRandom(self,number=4,start_time=0.2,end_time=0.3):
        self.moveTo()
        self.click()
        temp = [self.up,self.down]
        for _ in range(number):
            f = random.choice(temp)
            f()
            self.wait(start_time,end_time)

    def __getitem__(self, item):
        if isinstance(self.element(),list):
            return self.element()[item]
        else:
            # 当前2.7小bug
            # return self.element()
            return [self.element()][item]

    def __len__(self):
        return self.elementNumber()

    def openTakeOver(self):
        path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(path,"take_over")

        if not os.path.isdir(file_path):
            os.mkdir(file_path)

        # 执行无效
        cmd = "chrome.exe --remote-debugging-port=9222 --user-data-dir=\"{}\"".format(file_path)
        os.system(cmd)

# chrome.exe --remote-debugging-port=9222 --user-data-dir="D:\code\my_python\PersonificationAuto\test_selenium"
op = {
    # "add_experimental_option":[("debuggerAddress","127.0.0.1:9222")]
}
# pa = PersonificationAuto(is_tracking_path=True)
# # with open("stealth.min.js") as f:
# #     js=f.read()
# # pa.driver().execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",{'source':js})
# # pa.openTakeOver()
# pa.setAge(18)
# pa.maxWin()
# # pa.get("https://www.runoob.com/sitemap")
# # mac下加载本地网页加file://
# # pa.get(r"D:\code\my_html\automationCode.html")
# # pa.get("https://login.taobao.com/member/login.jhtml")
#
