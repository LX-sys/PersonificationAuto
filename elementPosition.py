# -*- coding:utf-8 -*-
# @time:2022/4/4 9:50
# Author:LX
# @File:elementPosition.py
# @Software:PyCharm
# import random
'''
    元素位置操作类
'''

from header import (
    json,
    random,
    WebDriver,
)


class ElementPosition(object):
    '''
        元素位置操作类
    '''
    def __init__(self, driver=None, ele=None,is_update_pos=True):
        # 坐标，宽高
        self.__pos = {"x": 0, "y": 0}
        self.__size = {'width': 0.0, 'height': 0.0}
        # 元素类型
        self.__tag_name = None

        if driver:
            self.setDriver(driver)
        else:
            self.__driver = None
        if ele:
            self.setElement(ele,is_update_pos=is_update_pos)
        else:
            self.__element = None


    # 设置驱动
    def setDriver(self,driver=None):
        if isinstance(driver, WebDriver):
            self.__driver = driver
        else:
            raise TypeError("It is not a WebDriver object")
        return self

    # 设置元素对象
    def setElement(self,ele=None,is_update_pos=True):
        self.__element = ele
        # 获取元素的位置信息,多个元素的情况下不获取
        if not isinstance(ele,list) and is_update_pos:
            self.__updatePos()
        return self

    # 返回元素对象
    def element(self):
        '''
            获取元素对象本身
        :return:
        '''
        return self.__element

    def setX(self,x=0):
        self.__pos["x"] = x
        return self

    def setY(self,y=0):
        self.__pos["y"] = y
        return self
    
    def setWidth(self,width=0.0):
        self.__size["width"] = width
        return self

    def setHeight(self,height=0.0):
        self.__size["height"] = height
        return self

    def setPos(self,x=None,y=None):
        if x:
            self.setX(x)
        if y:
            self.setY(y)
        return self
    
    def setSize(self,width=None,height=None):
        if width:
            self.setWidth(width)
        if height:
            self.setHeight(height)
        return self

    def setRect(self,x=None,y=None,width=None,height=None):
        self.setPos(x,y)
        self.setSize(width,height)
        return self

    # 更新元素位置
    def __updatePos(self,is_test=False):
        # JS代码
        if is_test:
            return
        try:
            js_code = """var r = arguments[0].getBoundingClientRect();
                                return {top: (window.outerHeight - window.innerHeight) + Math.floor(r.top),
                                left: Math.floor(r.left), elem_width: r.width, elem_height: r.height}"""
            res = self.__driver.execute_script(js_code, self.element())
            width = round(res['elem_width'],2)
            height = round(res['elem_height'],2)
            x = res['left'] + random.randint(int(res['elem_width']) // random.randint(2, 3),
                                             int(res['elem_width'] * 2 // 3))
            y = res['top'] + random.randint(int(res['elem_height']) // 3,
                                            int(res['elem_height'] * 2 // 3))
            # 记录，坐标，宽高
            self.setRect(x, y, width, height)
        except:
            self.setRect(0, 0, 0.0, 0.0)

    def rect(self,is_cache=True):
        if is_cache:
            self.__updatePos()
        return {"x":self.x(),
                "y":self.y(),
                'width':round(self.width(),2),
                'height':round(self.height(),2)}

    # 元素中心位置
    def centerPos(self):
        return self.x()+round(self.width(),2)//2,self.y()+round(self.height(),2)//2

    def x(self,is_cache=True):
        if is_cache:
            self.__updatePos()
        return self.__pos["x"]

    def y(self,is_cache=True):
        if is_cache:
            self.__updatePos()
        return self.__pos["y"]

    def width(self,is_cache=True):
        if is_cache:
            self.__updatePos()
        return self.__size["width"]

    def height(self,is_cache=True):
        if is_cache:
            self.__updatePos()
        return self.__size["width"]

    def setShape(self,tag_name):
        self.__tag_name = tag_name
        return self

    def shape(self,is_test=False):
        if is_test:
            return self.__tag_name
        self.setShape(self.element().tag_name)
        '''
            元素的形状
            你当前获取元素的标签名:
            例如: input,h1,a
        :return:str
        '''
        return self.__tag_name

    @property
    def value(self):
        return self.element().get_attribute('value')

    @property
    def text(self):
        return self.element().text

    @property
    def length(self):
        try:
            return self.__driver.execute_script("return arguments[0].length;", self.element())
        except:
            return 0

        # def __repr__(self):
    #     return repr({"x":self.x(),"y":self.y(),
    #                  "width":self.width(),"height":self.height()})
    
    # def __str__(self):
    #     return str(type(self))
    
    def __getitem__(self,item):
        if item.lower() == "x":
            return self.x()
        elif item.lower() == "y":
            return self.y()
        elif item.lower() == "width" or item.lower() == "w":
            return self.width()
        elif item.lower() == "height" or item.lower() == "h":
            return self.height()
        else:
            if isinstance(self.__element,list):  # 如果是list则使用自身的类进行构建,为了提高速度,不获取信息
                return ElementPosition(self.__driver,self.__element[item],is_update_pos=False)
            return self.__element

    # 重载减法,得到两个元素之间的距离
    def __sub__(self, other):
        return {"x":self.x()-other.x(),"y":self.y()-other.y()}

    # 重载等于,比较两个元素是否属于同一类型
    def __eq__(self, other):
        return self.shape() == other.shape()

    # def equalPos(self,other):
    #     if self.x()

if __name__ == '__main__':
    e = ElementPosition()
    e.setElement([1,2,3])
    for e_i in e:
        print(e_i)
        # print e_i

    # e.setRect(100,100,10.3,5.1)
    # e1 = ElementPosition()
    # e1.setRect(150, 150, 10.3, 5.1)
    # print e1-e
    # print e.elementNumber()
    # print e["x"],e["y"],e["width"],e["height"]
    # print e
