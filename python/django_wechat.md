# django 微信公众号开发 - 获取授权,绑定用户微信 openid

通过授权获得用户 openid，可以跟用户进行后续交互，主动推送消息等。

参考：
https://developers.weixin.qq.com/doc/offiaccount/OA_Web_Apps/Wechat_webpage_authorization.html
https://segmentfault.com/a/1190000021719807

特别注意：这个必须要微信公众号（个人的订阅号不能用这个功能）进行了微信认证才能使用。还有回调域名需要是 https 的，可以使用 Let's Encrypt 申请到免费 https 证书。

## 数据库（Model）建立保存用户 openid 的字段

因为我们让用户授权的目的就是得到 openid，获得 openid 后要存到数据库中，并和用户建立对应关系。

我用的是 django 自带的用户系统，官方推荐建立一个自定义的 UserProfile 之类的 Model 保存用户相关信息。

```
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, default=None)
    openid = models.CharField("微信 openid", max_length=32)
```

openid 的长度貌似是 28 位，这里定义的最大长度 32 应该够用。

[参考](https://link.segmentfault.com/?enc=YGfN9zdyZ5fS99yluCJ6RQ%3D%3D.emfAVX2boeBd6GxM7%2BuaqPfJBhG3qxb63X6p9cl1g0ZJXBQWL%2BPwZDFLVbNiuLfp)

## 跳转到用户授权页面

这个页面是微信的页面，需要我们加上参数，让用户跳转过去，url 是

https://open.weixin.qq.com/connect/oauth2/authorize?appid=APPID&redirect_uri=REDIRECT_URI&response_type=code&scope=SCOPE&state=STATE#wechat_redirect

appid 去公众号平台 - > 开发 -> 基本配置 里找。

redirect_uri 是成功以后的回调地址，是你自己的一个 url，要通过 urlEncode 进行编码

response_type 写 code

scope 可选填 snsapi_base 或 snsapi_userinfo

state 非必填，所以直接不加这个参数了

关于 python 的 urlEncode 可以使用：

import urllib.parse
s='https://xxx.com/api/weixin_bind_callback/'
urllib.parse.quote(s)

结果是：`'https%3A//xxx.com/api/weixin_bind_callback/'`

它没有处理斜杠，添加一个 safe 参数就可以处理斜杠了

import urllib.parse
s='https://xxx.com/api/wexin_bind_callback/'
urllib.parse.quote(s, safe='')

结果是：`'https%3A%2F%2Fxxx.com%2Fapi%2Fwexin_bind_callback%2F'`

我的这个 url 的最终结果是：

https://open.weixin.qq.com/connect/oauth2/authorize?appid=XXXX&redirect_uri=https%3A%2F%2FXXXX.com%2Fweixin%2Fbind%2Fcallback%2F&response_type=code&scope=snsapi_userinfo#wechat_redirect

## 用户授权后通过 code 获取 access_token

下面的逻辑要写在上面给用户访问的 url 里的回调的页面里。

请求 url 是：

`https://api.weixin.qq.com/sns/oauth2/access_token?appid=APPID&secret=SECRET&code=CODE&grant_type=authorization_code`

APPID 和 secret 去公众号平台 - > 开发 -> 基本配置 里找。

code 是返回的 code

grant_type 就写 authorization_code

这里需要使用 http 客户端库，例如 python3 的 requests 或者 python2 的 urllib2，请求微信的接口

python3 的例子：

import requests
APPID = ''
secret = ''

r = requests.get('https://api.weixin.qq.com/sns/oauth2/access_token?appid=APPID&secret=SECRET&code=CODE&grant_type=authorization_code')

请求结果是：
```

{
  "access_token":"ACCESS_TOKEN",
  "expires_in":7200,
  "refresh_token":"REFRESH_TOKEN",
  "openid":"OPENID",
  "scope":"SCOPE" 
}

```
这时候需要再发起一次请求才能得到用户的信息。

这次的请求 url：

`https://api.weixin.qq.com/sns/userinfo?access_token=ACCESS_TOKEN&openid=OPENID&lang=zh_CN`

这个返回的结果是：
```

{   
  "openid":" OPENID",
  "nickname": NICKNAME,
  "sex":"1",
  "province":"PROVINCE",
  "city":"CITY",
  "country":"COUNTRY",
  "headimgurl":       "http://thirdwx.qlogo.cn/mmopen/g3MonUZtNHkdmzicIlibx6iaFqAc56vxLSUfpb6n5WKSYVY0ChQKkiaJSgQ1dZuTOgvLLrhJbERQQ4eMsv84eavHiaiceqxibJxCfHe/46",
  "privilege":[ "PRIVILEGE1" "PRIVILEGE2"     ],
  "unionid": "o6_bmasdasdsad6_2sgVt7hMZOPfL"
}

```

最终的 view 是：

```
def weixinbind_callback(request):
    code = request.GET.get('code')
    state = request.GET.get('state')
    # print(code, state)
    APPID = 'xxxxxx'
    secret = 'xxxxx'
    r = requests.get(
        'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code' % (APPID, secret, code)
    )
    print(r.text)
    d = json.loads(r.text)
    # {
    #   "access_token":"ACCESS_TOKEN",
    #   "expires_in":7200,
    #   "refresh_token":"REFRESH_TOKEN",
    #   "openid":"OPENID",
    #   "scope":"SCOPE"
    # }
    r = request.get(
        'https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN' % (d['access_token'], d['openid'])
    )
    # print(r.text)
    dd = json.load(r.text)
    # {
    #   "openid":" OPENID",
    #   "nickname": NICKNAME,
    #   "sex":"1",
    #   "province":"PROVINCE",
    #   "city":"CITY",
    #   "country":"COUNTRY",
    #   "headimgurl":       "http://thirdwx.qlogo.cn/mmopen/g3MonUZtNHkdmzicIlibx6iaFqAc56vxLSUfpb6n5WKSYVY0ChQKkiaJSgQ1dZuTOgvLLrhJbERQQ4eMsv84eavHiaiceqxibJxCfHe/46",
    #   "privilege":[ "PRIVILEGE1" "PRIVILEGE2"     ],
    #   "unionid": "o6_bmasdasdsad6_2sgVt7hMZOPfL"
    # }
    request.user.userprofile.openid = dd['openid']
    request.user.userprofile.nickname = dd['nickname']
    request.user.userprofile.wsex = dd['sex']
    request.user.userprofile.province = dd['province']
    request.user.userprofile.city = dd['city']
    request.user.userprofile.country = dd['country']
    request.user.userprofile.headimgurl = dd['headimgurl']
    request.user.userprofile.privilege = dd['privilege']
    request.user.userprofile.unionid = dd['unionid']
    request.user.userprofile.save()
    return HttpResponseRedirect('/weixin/')

```


## 添加回调域名

到公众号平台 设置-> 公众号设置 -> 功能设置 -> 网页授权域名 的配置选项中，把刚刚的回调的 url 的域名添加上，有一个认证文件。

他说要把文件传到服务器上，但是这个对于 django 不太方便，可以直接写一个 view 返回这个文件内容就可以了，我直接放到 urls 文件里了。

```
from django.urls import path
from django.http import HttpResponse

def weixin_verify(request):
    return HttpResponse('PJRLUusp1NXyuD70')


urlpatterns = [
    # 功能页面
    path('weixin/', account.views.weixin_page),
    
    # 微信授权页
    path('weixin/bind/', account.views.weixinbind),

    # 授权成功回调页
    path('weixin/bind/callback/', account.views.weixinbind_callback),
    
    path('MP_verify_PJRLUusp1NXyuD70.txt', weixin_verify),
]
```


## 最终代码总览

### urls.py

```
from django.urls import path
from django.http import HttpResponse

def weixin_verify(request):
    return HttpResponse('PJRLUusp1NXyuD70')

urlpatterns = [
    # 微信开发
    path('weixin/', account.views.weixin_page),
    path('weixin/bind/', account.views.weixinbind),
    path('weixin/bind/callback/', account.views.weixinbind_callback),
    path('MP_verify_PJRLUusp1NXyuD70.txt', weixin_verify),


]

### views.py

import requests
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import time
import json

def weixin_page(request):
    return render(request, 'weixin_index.html')

def weixinbind(request):
    return HttpResponseRedirect('https://open.weixin.qq.com/connect/oauth2/authorize?appid=XXXXX&redirect_uri=https%3A%2F%2FXXXXX.com%2Fweixin%2Fbind%2Fcallback%2F&response_type=code&scope=snsapi_userinfo#wechat_redirect')

def weixinbind_callback(request):
    code = request.GET.get('code')
    state = request.GET.get('state')
    print(code, state)
    APPID = 'xxxxx'
    secret = 'xxxxx'
    r = requests.get(
        'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code' % (APPID, secret, code)
    )
    print(r.text)
    d = json.loads(r.text)
    # {
    #   "access_token":"ACCESS_TOKEN",
    #   "expires_in":7200,
    #   "refresh_token":"REFRESH_TOKEN",
    #   "openid":"OPENID",
    #   "scope":"SCOPE"
    # }
    r = requests.get(
        'https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN' % (d['access_token'], d['openid'])
    )
    print(r.content)
    dd = json.loads(r.content.decode('utf8'))
    # {
    #   "openid":" OPENID",
    #   "nickname": NICKNAME,
    #   "sex":"1",
    #   "province":"PROVINCE",
    #   "city":"CITY",
    #   "country":"COUNTRY",
    #   "headimgurl":       "http://thirdwx.qlogo.cn/mmopen/g3MonUZtNHkdmzicIlibx6iaFqAc56vxLSUfpb6n5WKSYVY0ChQKkiaJSgQ1dZuTOgvLLrhJbERQQ4eMsv84eavHiaiceqxibJxCfHe/46",
    #   "privilege":[ "PRIVILEGE1" "PRIVILEGE2"     ],
    #   "unionid": "o6_bmasdasdsad6_2sgVt7hMZOPfL"
    # }
    request.user.userprofile.openid = dd['openid']
    request.user.userprofile.nickname = dd['nickname']
    request.user.userprofile.wsex = dd['sex']
    request.user.userprofile.province = dd['province']
    request.user.userprofile.city = dd['city']
    request.user.userprofile.country = dd['country']
    request.user.userprofile.headimgurl = dd['headimgurl']
    request.user.userprofile.privilege = json.dumps(dd['privilege'])
    #request.user.userprofile.unionid = dd['unionid']
    request.user.userprofile.refresh_token_time = time.time()
    request.user.userprofile.save()
    return HttpResponseRedirect('/weixin/')

### models.py

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, default=None)
    # 微信开发
    openid = models.CharField("微信 openid", max_length=32, default='')
    nickname = models.CharField("微信昵称", max_length=256, default='')
    wsex = models.CharField("微信性别", max_length=3, default='')
    province = models.CharField("微信省份", max_length=50, default='')
    city = models.CharField("微信城市", max_length=50, default='')
    country = models.CharField("微信国家", max_length=50, default='')
    headimgurl = models.CharField("微信头像", max_length=200, default='')
    privilege = models.CharField("微信权限", max_length=3, default='')
    unionid = models.CharField("微信 unionid", max_length=32, default='')
    refresh_token = models.CharField("微信 refresh_token", max_length=512, default='')
    refresh_token_time = models.IntegerField(default=0)
```


html 部分省略了

## 错误解决

微信登录失败 redirect_uri域名与后台配置不一致，错误码10003

到公众号平台 设置-> 公众号设置 -> 功能设置 -> 网页授权域名 的配置选项中，修改授权回调域名。

见上文 添加回调域名。
