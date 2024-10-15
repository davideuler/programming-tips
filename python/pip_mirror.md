
## 清华
https://mirrors.tuna.tsinghua.edu.cn/help/pypi/

pip
临时使用
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple some-package
注意，simple 不能少, 是 https 而不是 http

设为默认
升级 pip 到最新的版本 (>=10.0.0) 后进行配置：

python -m pip install --upgrade pip
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
如果您到 pip 默认源的网络连接较差，临时使用本镜像站来升级 pip：

python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip

## 南方科技大

pip install --upgrade pip --index-url https://mirrors.sustech.edu.cn/pypi/web/simple
pip config set global.index-url https://mirrors.sustech.edu.cn/pypi/web/simple


## 阿里云

https://mirrors.aliyun.com/pypi/simple