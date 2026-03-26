
## Docker desktop need a HTTP proxy to pull image from Docker hub.

And I need to convert my local socks5 proxy to http.

### Options:
https://github.com/zhanglei002/socks2http

Change the ports in socks2http3.py, and start the agent:

```
python3 socks2http3.py
```

### Other Options:
https://github.com/KaranGauswami/socks-to-http-proxy

https://github.com/oyyd/http-proxy-to-socks

https://github.com/qwj/python-proxy

### Example to 

```
wget https://github.com/KaranGauswami/socks-to-http-proxy/releases/download/v0.3.0/sthp-macos
chmod +x sthp-macos
sthp -p 8080 -s 127.0.0.1:1080
# This will create proxy server on 8080 and use localhost:1080 as a Socks5 Proxy

socks2http in rust does not work as a proxy for docker pull, it will timeout.

```

### 设置 Docker 使用 v2sub/v2ray 的 proxy 加速 docker pull，设置 docker 镜像仓库

vim /etc/docker/daemon.json

```
{
    "runtimes": {
        "nvidia": {
            "args": [],
            "path": "nvidia-container-runtime"
        }
    },
    "registry-mirrors": [
        "https://docker.1panel.live",
        "https://hub.rat.dev",
        "https://docker.m.daocloud.io",
        "https://dockerproxy.com"
    ],

    "proxies": {
            "http-proxy": "http://10.0.0.145:1081",
            "https-proxy": "http://10.0.0.145:1081",
            "no-proxy": "*.cn,*.aliyun.com,*.aliyuncs.com,*.163.com,*.baiduce.com,*.qiniu.com，*.daocloud.io,127.0.0.0/8,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16,100.64.0.0/10"
    }
}
```

Restart docker daemon
```
sudo systemctl restart docker
```

