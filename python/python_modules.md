

## Failed to run file in a submodule 

```
python pyapi/keyword.py
```
ImportError: No module named dirFoo1.foo1



Set your PYTHONPATH environment variable. For example like this PYTHONPATH=.:.. (for *nix family).

Also you can manually add your current directory (src in your case) to pythonpath:

import os
import sys
sys.path.insert(0, os.getcwd())

## Enable simple default logging

``` python
import logging

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

# 记录下来 行号 文件名:方法名
logging.basicConfig(filename='application.log', level=logging.INFO, format='%(asctime)s - %(levelname)-5s %(lineno)d %(filename)s:%(funcName)s - %(message)s')

logger = logging.getLogger(__name__)
```

## Logging by Loguru

https://github.com/Delgan/loguru


## Get current function name 

function_name = sys._getframe().f_code.co_name

``` python
import sys

def query_database():
    function_name = sys._getframe().f_code.co_name
    logger.info("Start %s()" % function_name)
    start_time = time.time()
    #.....
    logger.info("%s() cost: %s " % (function_name, time.time() - start_time) )

```

## Dynamically replace a method of third-party library.

For example, repace the werobot get_access_token method to use a customized method which stores token in redis, 
and share the token across processes.

```
from werobot.client import Client

## 覆盖 Client 类中的 get_access_token 方法，存储 token 信息到 redis
from client_shared import get_shared_access_token

Client.get_access_token = get_shared_access_token
```


## Call a function dynamically by function name

``` python
# I have this code:

fields = ['name','email']

def clean_name():
    pass

def clean_email():
    pass

# How can I call clean_name() and clean_email() dynamically?


Solution based on none class and class:

``` python
  # method 1
        function = getattr(sys.modules[__name__], function_name)  # or you can use module name instead of __main__
        return function(text)  # calls my_function and outputs "Hello, world!"
        
  # method 2, mapp function to values in dictionary
  fields = {'name':clean_name,'email':clean_email}

  for key in fields:
    fields[key]()
  
# method 3, class
#  You could even move further and do something like this:

class Cleaner(object):
    def __init__(self, fields):
        self.fields = fields

    def clean(self):
        for f in self.fields:
            getattr(self, 'clean_%s' % f)()

# Then inherit it and declare your clean_<name> methods on an inherited class:

cleaner = Cleaner(['one', 'two'])
cleaner.clean()

```

## Current time and date

``` python
week_list = ["星期一","星期二","星期三","星期四","星期五","星期六","星期日"]

def current_time(prompt):
    unix_time = time.time()
    text = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S')
    return "现在的时间是: %s" % text

def current_date(prompt):
    today = date.today()
    text = date.strftime(today, "%Y年%m月%d日")
    return "今天是: %s" % text
    
def current_day(prompt):
    today = datetime.today()
    # 使用strftime()方法将今天的日期格式化为星期几的字符串
    weekday = week_list[today.weekday()]
    return "今天%s" % weekday
```
