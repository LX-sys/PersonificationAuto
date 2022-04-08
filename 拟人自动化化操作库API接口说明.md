[TOC]

# PersonificationAuto

```
拟人自动化操作库
```

### 编写语言版本

```
Python2.7
```

### 作者

```
LX
```

### 所有类

```
ElementPosition     -->元素位置类（其次）
PersonificationAuto -->拟人化操作类(中等关注的类)
Log                 -->日志类
```

### ElementPosition API接口

##### `__init__(self, driver=None, ele=None,is_update_pos=True):`

```
ElementPosition操作元素所有的信息
功能说明:
	初始化
参数说明
    driver: 浏览器驱动对象(默认None)
    ele: 元素对象(默认None)
    is_update_pos:是否在拿到后立即获取位置信息
```

##### setDriver(driver=None)

```python
功能说明:
    设置浏览器驱动
参数说明
    driver: 浏览器驱动对象
```

##### setElement(ele,is_update_pos=True)

```python
功能说明:
    设置元素
参数说明
    ele: 元素对象
    is_update_pos:是否在拿到后立即获取位置信息
# --------------例子
ele = dirver.find_element(xx,xx)
xx.setElement(dirver.find_element(xx,xx))
```

##### element()

```python
功能说明:
    返回元素对象本身
返回类型:
    WebElement
```

##### setX(x=0)

```python
功能说明:
    设置元素x位置坐标
参数说明:
    x: X轴坐标点(类型int)
```

##### setY(y=0)

```python
功能说明:
    设置元素y位置坐标
参数说明:
    y: y轴坐标点(类型int)
```

##### setWidth(width=0.0)

```python
功能说明:
    设置元素width位置坐标
参数说明:
    width: 元素宽度(类型float)
```

##### setHeight(height=0.0)

```python
功能说明:
    设置元素height位置坐标
参数说明:
    height: 元素高度(类型float)
```

##### setPos(x=None,y=None):

```python
功能说明:
    设置元素(x,y)位置坐标
参数说明:
    x: X轴坐标点(类型int)
    y: y轴坐标点(类型int)
# ------
注意这里也可以只给一个参数
```

##### setSize(width=None,height=None):

```python
功能说明:
    设置元素的大小
参数说明:
    width: 元素宽度(类型float)
    height: 元素高度(类型float)
# ------
注意这里也可以只给一个参数
```

##### setRect(x=None,y=None,width=None,height=None):

```python
功能说明:
    设置元素的四项基础属性
参数说明:
	x: X轴坐标点(类型int)
    y: y轴坐标点(类型int)
    width: 元素宽度(类型float)
    height: 元素高度(类型float)
# ------
注意这里也可以只给任意一个参数或者任意多个参数
```

##### rect(is_cache=True):

```python
功能说明:
    获取元素的四项基础属性
参数说明:
    is_cache:是否从缓存中拿去属性信息(默认不从缓存拿数据,会再次根据元素去拿最新数据)
返回类型:
    json,dict
返回格式:
    {"x":xx"y":xx,"width":xxx,"height":xxx}
```

##### centerPos()

```python
功能说明:
    返回元素中心位置
返回类型:
    int
```

##### x(is_cache=True)

```python
功能说明:
    返回元素x坐标
参数说明:
    is_cache:是否从缓存中拿去属性信息(默认不从缓存拿数据,会再次根据元素去拿最新数据)
```

##### y(is_cache=True)

```python
功能说明:
    返回元素y坐标
参数说明:
    is_cache:是否从缓存中拿去属性信息(默认不从缓存拿数据,会再次根据元素去拿最新数据)
```

##### width(is_cache=True)

```python
功能说明:
    返回元素宽度
参数说明:
    is_cache:是否从缓存中拿去属性信息(默认不从缓存拿数据,会再次根据元素去拿最新数据)
```

##### height(is_cache=True)

```python
功能说明:
    返回元素高度
参数说明:
    is_cache:是否从缓存中拿去属性信息(默认不从缓存拿数据,会再次根据元素去拿最新数据)
```

##### setShape(,tag_name)

```python
功能说明:
    设置元素的形状(例如: input,a,h1,h2,...)
```

##### shape()

```python
功能说明:
    返回元素的形状(例如: input,a,h1,h2,...)
返回类型:
    string
```

##### value()

```python
功能说明:
    返回元素的值
返回类型:
    string
# ------------------
注意:这个是属性的调用方式,后面不需要加()
```

##### text()

```python
功能说明:
    返回元素所包含的文本信息
返回类型:
    string
# ------------------
注意:这个是属性的调用方式,后面不需要加()
```

##### length()

```python
功能说明:
    返回元素的长度
返回类型:
    int
# ------------------
注意:这个是属性的调用方式,后面不需要加()
对select下拉框有非常显著的效果
```

##### ElementPosition 其他信息

```python
ElementPosition对象之前支持减法,和==，支持下标操作(但是只支持基础的四项属性x,y,width,height,宽高可以使用开头字母或者全拼)
# ---例子
a = ElementPosition(x,x)
b = ElementPosition(x,x)
c = b-c  # c的结构是{"x":xx,"y":xx}

a==b  # 这里比较的是它们形状,看它们是否属于同一类元素

例如获取x的坐标
常规操作 a.x()
下标操作 a["x"],a["width"],a["w"]
```

### PersonificationAuto API接口

#####  `_init__(self,driver=None,executable_path="chromedriver.exe",options=None,age=None,is_log=False,log_path=None,is_tracking_path=False,start_time=0.0,end_time=0.0)`

```python
PersonificationAuto
	这个类主要是模拟人来操作浏览器
功能说明:
	初始化
参数说明:
    driver: 浏览器驱动对象(默认None)
    executable_path: 浏览器驱动(默认谷歌)(类型string)
    options: 配置信息(类型list)
    age: 操作人年龄(类型int)
    is_tracking_path:是否显示行动轨迹(类型bool)
    start_time: 随机等待的开始时间(类型float)
    end_time: 随机等待的结束时间(类型float)
```

##### lookOptionList()

```python
功能说明:
	返回常见的配置信息
返回类型:
    list
```

##### setErrorLimit(limit=None)

```python
功能说明:
    设置显示错误的最大深度
参数说明:
    limit:深度(类型int)
# --------------
注意这个功能使用前提，是必须开启显示行动轨迹(在__init__里面)，
如果你设置的深度超过了系统最大深度，则以系统为准
```

##### setAge(age=15)

```python
功能说明:
    设置操作人的年龄,年龄决定鼠标移动的速度
参数说明:
    age: 年龄(类型int)
```

##### setMouseSpeed(min_speed,max_speed):

```python
功能说明:
    设置鼠标移动速度
参数说明:
    min_speed: 最小速度(类型float)
    max_speed: 最大速度(类型float)
 # ------------------------
 注意这个速度一般不需要手动设置，会跟随年龄自动变化
```

##### age()

```python
功能说明:
    返回当前年龄
 返回类型:
    int
```

##### getLogObj()

```
功能说明:
	获取日志对象
返回类型:
	Log
```

##### elementNumber()

```python
功能说明:
    返回元素的个数
返回类型:
    int
```

##### mouseSpeed()

```python
功能说明:
    返回当前鼠标移动速度
 返回类型:
    list
 格式说明:
 	[flost,flost]
```

##### maxWin()

```python
功能说明:
    浏览器窗口最大化
```

##### minWin()

```
功能说明:
    浏览器窗口最小化
```

##### currentTime( connector_before=":", connector_after=":",custom=None):

```python
功能说明:
    返回当前格式化时间
参数说明:
    connector_before: 年月日之间连接符
    connector_after: 时分秒之间连接符
    custom: 自定义日期格式
返回类型:
    string
返回格式:
    Y:m:d H:M:S
```

##### element()

```python
功能说明:
    返回元素位置对象
返回类型:
	如果单个元素,则类型是ElementPosition
    如果是多个元素,则类型是list
# --------------------
在Pycharm用这个函数去点去点其他函数时,可能会出现报黄,
这是因为返回值不统一造成的,而且在python2.7中也无法添加返回类型注释
```

##### driver()

```python
功能说明:
    返回浏览器驱动对象
返回类型:
    WebDriver
```

##### setElement(ele)

```python
功能说明:
    设置元素
参数说明
    ele: 元素对象
```

##### get(url)

```python
功能说明:
    请求网站
参数说明:
    url: 网址(类型string)
```

##### log(path="",connector=":")

```python
功能说明:
    在本地生成日志
参数说明:
    path:日志存放路径(类型string)
    connector:日期之间的连接符号(类型string)
```

##### autoMatch(paths_type,paths):

```python
功能说明:
    根据多种或者一种匹配方式进行匹配元素
参数说明:
    paths_type: 匹配方式(类型str或者list)
    paths:匹配路径(类型str或者list)
# -----------------------------------------------
多对一
多对多
一对多
xx.autoMatch(["id","xpath"],"xxx")
xx.autoMatch(["xpath","xpath"],["xxx","xxxx"])
xx.autoMatch("id",["xxx","xxxx"])
```

##### id(path,start_time=None,end_time=None,note=""):

```python
功能说明:
    使用ID方式查找元素
参数说明:
    id: 元素ID(类型string或者list)
    start_time: 随机等待的开始时间(类型float)
    end_time: 随机等待的结束时间(类型float)
    note: 备注
# -----------------------------
一对一
一对多
其他匹匹配方式同理
xx.id("xxx")
xx.id(["xx","xx",...])
可以传一个单独的匹配规则,
也可以将可能出现的多个匹配规则传入(但是在找到第一个匹配成功的规则时,立刻返回，后面将不在匹配)
```

##### xpath(path,start_time=None,end_time=None,note=""):

```python
功能说明:
    使用xpath方式查找元素
参数说明:
    xpath: 元素xpath(类型string)
    start_time: 随机等待的开始时间(类型float)
    end_time: 随机等待的结束时间(类型float)
    note: 备注
# -----------------------------
可以传一个单独的匹配规则,
也可以将可能出现的多个匹配规则传入(但是在找到第一个匹配成功的规则时,立刻返回，后面将不在匹配)
```

##### className(path,start_time=None,end_time=None,note=""):

```python
功能说明:
    使用class方式查找元素
参数说明:
    class: 元素class(类型string)
    start_time: 随机等待的开始时间(类型float)
    end_time: 随机等待的结束时间(类型float)
    note: 备注
# -----------------------------
可以传一个单独的匹配规则,
也可以将可能出现的多个匹配规则传入(但是在找到第一个匹配成功的规则时,立刻返回，后面将不在匹配)
```

##### css(path,start_time=None,end_time=None,note=""):

```python
功能说明:
    使用css方式查找元素
参数说明:
    class: 元素class(类型string)
    start_time: 随机等待的开始时间(类型float)
    end_time: 随机等待的结束时间(类型float)
    note: 备注
# -----------------------------
可以传一个单独的匹配规则,
也可以将可能出现的多个匹配规则传入(但是在找到第一个匹配成功的规则时,立刻返回，后面将不在匹配)
```

##### cssSelector(path,start_time=None,end_time=None,note=""):

```python
功能说明:
    使用css selector方式查找元素
参数说明:
    class: 元素class(类型string)
    start_time: 随机等待的开始时间(类型float)
    end_time: 随机等待的结束时间(类型float)
    note: 备注
# -----------------------------
可以传一个单独的匹配规则,
也可以将可能出现的多个匹配规则传入(但是在找到第一个匹配成功的规则时,立刻返回，后面将不在匹配)
```

##### linkText(path,start_time=None,end_time=None,note=""):

```python
功能说明:
    使用link text方式查找元素
参数说明:
    class: 元素class(类型string)
    start_time: 随机等待的开始时间(类型float)
    end_time: 随机等待的结束时间(类型float)
    note: 备注
# -----------------------------
可以传一个单独的匹配规则,
也可以将可能出现的多个匹配规则传入(但是在找到第一个匹配成功的规则时,立刻返回，后面将不在匹配)
```

##### linkTextPartial(path,start_time=None,end_time=None,note=""):

```python
功能说明:
    使用partial link text方式查找元素
参数说明:
    class: 元素class(类型string)
    start_time: 随机等待的开始时间(类型float)
    end_time: 随机等待的结束时间(类型float)
    note: 备注
# -----------------------------
可以传一个单独的匹配规则,
也可以将可能出现的多个匹配规则传入(但是在找到第一个匹配成功的规则时,立刻返回，后面将不在匹配)
```

##### moveTo(x=None,y=None,_time=None):

```python
功能说明:
    移动到元素位置
    如果不传值,可以自动计算位置,移动的时间可以跟随年龄而变化
参数说明:
    x: x坐标(类型int)
    y: y坐标(类型int)
    _time: 鼠标移动时间
```

##### send_keys(str_data,trend_mode=1,trend_speed=0.2,is_click=False,is_clear=False,is_verify=True):

```python
功能说明:
    输入数据
参数说明:
    str_data: 输入的数据(类型string)
    trend_mode: 输入数据的模式 递增：1 递减: 2 匀速: 3(类型int)
    trend_speed: 影响递增，递减的数值(类型float)
    is_click: 输入前是否点击(类型bool)
    is_clear: 输入前是否先清空原本的数据(类型bool)
    is_verify:验证数据是真的输入了(只会验证一次)
```

##### click(number=1,start_time=0.2,end_time=0.4,is_move=True):

```python
功能说明:
    鼠标左键按下
参数说明:
    number: 点击的次数(类型int)
    start_time: 鼠标点击时间随机间隔开始
    end_time: 鼠标点击时间随机间隔结束
    is_move: 点击前是否先移动
```

##### rightClick(number=1,start_time=0.2,end_time=0.4,is_move=True):

```python
功能说明:
    鼠标右键按下
参数说明:
    number: 点击的次数(类型int)
    start_time: 鼠标点击时间随机间隔开始
    end_time: 鼠标点击时间随机间隔结束
    is_move: 点击前是否先移动
```

##### LeftDoubleClick(number=1,start_time=0.2,end_time=0.4,is_move=True):

```python
功能说明:
    鼠标左键双击
参数说明:
    number: 点击的次数(类型int)
    start_time: 鼠标点击时间随机间隔开始
    end_time: 鼠标点击时间随机间隔结束
    is_move: 点击前是否先移动
```

##### enter(start_time=0.0,end_time=0.0):

```python
功能说明:
    键盘回车
参数说明:
    start_time: 回车前随机等待开始
    end_time: 回车前随机等待结束
```

##### tab(start_time=0.0,end_time=0.0):

```python
功能说明:
    键盘Tab键
参数说明:
    start_time: Tab前随机等待开始
    end_time: Tab前随机等待结束
```

##### scroll(value=40,start_time=2, end_time=2,direction="bottom")

```
功能说明:
	浏览器滚动条
参数说明:
	value: 滚动条滚动的距离(类型int)
	start_time: 在多少秒完成滚动的随机时间开始(类型int)
	end_time：在多少秒完成滚动的随机时间结束(类型int)
	direction: 方向(类型string)(默认向下滚动)
		bottom:下
		top:上
		left: 左
		right:右
```

##### scrollBottom(start_time=1, end_time=1)

```python
功能说明:
    滚动条到底端
参数说明:
	start_time: 在多少秒完成滚动的随机时间开始(类型int)
	end_time：在多少秒完成滚动的随机时间结束(类型int)
```

##### scrollTop(start_time=1, end_time=1)

```python
功能说明:
    滚动条到顶端
参数说明:
	start_time: 在多少秒完成滚动的随机时间开始(类型int)
	end_time：在多少秒完成滚动的随机时间结束(类型int)
```

##### scrollLeft(start_time=1, end_time=1)

```
功能说明:
	滚动到浏览器最左端
参数说明:
	start_time: 在多少秒完成滚动的随机时间开始(类型int)
	end_time：在多少秒完成滚动的随机时间结束(类型int)
```

##### scrollRight(start_time=1, end_time=1)

```python
功能说明:
	滚动到浏览器最右端
参数说明:
	start_time: 在多少秒完成滚动的随机时间开始(类型int)
	end_time：在多少秒完成滚动的随机时间结束(类型int)
```

##### wait(start_time=None,end_time=None):

```python
功能说明:
    强制等待
参数说明:
    start_time: 随机等待时间开始
    end_time: 随机等待时间结束
```

##### quit(start_time=None,end_time=None)

```python
功能说明:
    退出浏览器
参数说明:
    start_time: 退出前浏览器等待的时间开始
    end_time: 退出前浏览器等待的时间结束
```

##### newElement(path_type,path):

```python
功能说明:
    创建一个新的ElementPosition对象
参数说明:
    path_type: 元素定位方式
    path: 对应方式的路径
返回类型:
    ElementPosition对象
# ------------------------------
例子:
    xxx.newElement('id','xx')
```

##### drag(x1,y1,x2,y2):

```python
功能说明:
    鼠标在坐标(x1,y2)出按下,(x2,y2)松开
参数说明:
    坐标(类型int)
    x1: 
    y1:
    x2:
    y2:
```

##### dragTo(x,y):

```python
功能说明:
    将元素拖拽到(x,y)坐标放下
参数说明:
    坐标(类型int)
    x: 
    y:
```

##### dragToDrop(newEle):

```python
功能说明:
    将元素拖拽到另一个元素位置方下
参数说明:
    newEle: 放置目标的元素对象(请使用newElement()方法去创建对象)
# ---------------------------------
例子:
    xx.dragToDrop(xxx.newElement('id','xx'))
```

##### frame()

```python
功能说明:
    进入iframe内嵌框架(进文档)
```

##### defaultContent()

```python
功能说明:
    切换到默认文档(相当于退出iframe内嵌框架)
```

##### goWin(index=0)

```
功能说明:
	切换到指定浏览器窗口
参数说明:
	index: 窗口索引,从0开始(类型int)
```

##### nextWin()

```
功能说明:
	切换到到浏览器下一个窗口
```

##### onWin():

```
功能说明:
	切换到到浏览器上一个窗口
```

##### refresh()

```python
功能说明:
    刷新浏览器
```

##### forward()

```python
功能说明:
    浏览器前进
```

##### back()

```python
功能说明:
    浏览器后退
```

##### closeWin()

```python
功能说明:
    关闭当前浏览器窗口
```

##### up(), down(), left(), right()

```python
功能说明:
    键盘上下左右
```

##### selectGetNumber(match_way,value)

```python
功能说明:
	获取select下拉框的项目数量
参数说明:
    match_way:匹配规则
        id
        class name
        tag name
  	value:规则所对应的值(这里就是html标签属性所对应的值)
返回类型:
    int
# ----------------------
例子:
    xx.selectGetNumber('id','xxx')
    xx.selectGetNumber('class name','xxx')
    xx.selectGetNumber('tag name','xxx')
```

##### selectGetText(match_way,value,index)

```python
功能说明:
	获取select下拉框指定下班的值
参数说明:
    match_way:匹配规则
        id
        class name
        tag name
  	value:规则所对应的值(这里就是html标签属性所对应的值)
    index:对应文本的下标(从0开始)
返回类型:
    string
```

##### selectRandom(number=4,start_time=0.2,end_time=0.3):

```python
功能说明:
    对选择框(仅限select写的)进行随机选择
参数说明:
    number: 选择的次数
    start_time: 每次选择的时间间隔开始
    end_time: 每次选择的时间间隔结束
```

### Log  API接口

##### `__init__(is_log=False,log_path=None)`

```python
功能说明:
    初始化
参数说明:
    is_log:是否启用日志(类型bool)
    log_path:日志存放的路径(类型string)
# ------------------------------
如果不启用日志,则设置路径无效
日志默认名称: recordPath.log
默认存放路径: 当前路径
```

##### setEnableLog(b_log)

```python
功能说明:
	是否启用日志
参数说明:
	b_log:(布尔类型bool)
		True:启用
		False:不启用
```

##### state()

```python
功能说明:
    获取日志的启用状态
 返回类型:
    布尔类型(bool)
```

##### setLogPath(path=".")

```python
功能说明:
    设置日志的存放路径
 参数说明:
    path:日志存放路径(类型string)
# ----------------
默认存放路径: 当前路径
注意设置路径时记得带上日志文件名称
例子:
    D:\xx\xx\test.log
```

##### log(path="",connector=":")

```python
功能说明:
    在本地生成日志
参数说明:
    path:日志存放路径(类型string)
    connector:日期之间的连接符号(类型string)
# ----------------------
这个一般不用这个类的log()
通常用PersonificationAuto这个类的log()
```

