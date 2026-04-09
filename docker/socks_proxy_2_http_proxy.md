
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

### Mac Colima 下面设置 Docker pull 的代理，

https://github.com/abiosoft/colima/issues/294
https://github.com/abiosoft/colima/issues/1040

```
colima start --edit

go to the last line

env: 
    http_proxy: http://192.168.5.2:7890
    https_proxy: http://192.168.5.2:7890
    no_proxy: localhost,192.168.5.2
quit then execute command

colima ssh sudo systemctl daemon-reload
colima ssh sudo systemctl restart docker
```
it works for me

### Mac Colima 下面设置 Docker Build 的代理

To set up a proxy for docker build in Colima, you must configure both the Colima VM environment (for pulling base images) and the Docker build arguments (for internet access during the build process). 
**1. Configure the Colima VM (System-wide)**
To ensure the Docker daemon inside the Colima VM can pull images through your proxy, edit the Colima configuration: 
Open the configuration: Run colima start --edit (or edit ~/.colima/default/colima.yaml).
Add environment variables: Locate the env: section and add your proxy settings:

``` yaml

env:
  HTTP_PROXY: http://your-proxy-address:port
  HTTPS_PROXY: http://your-proxy-address:port
  NO_PROXY: localhost,127.0.0.1,192.168.5.2
```

Note: If your proxy is running on your host machine (Mac/Linux), use the gateway IP 192.168.5.2 instead of localhost in the proxy URL. 
GitHub
GitHub
 
**2. Pass Proxy to the Build Process**
Configuring the VM environment often does not automatically pass proxy settings into the docker build container. You must provide them as build arguments: 
bash
docker build \
  --build-arg http_proxy=http://192.168.5.2:port \
  --build-arg https_proxy=http://192.168.5.2:port \
  --build-arg no_proxy=localhost,127.0.0.1 \
  -t your-image-name .
  
**3. Alternative: Global Docker Client Config**
Instead of flags, you can set the proxy globally for all builds in your host's Docker configuration file (~/.docker/config.json): 

``` json
{
 "proxies": {
   "default": {
     "httpProxy": "http://192.168.5.2:port",
     "httpsProxy": "http://192.168.5.2:port",
     "noProxy": "localhost,127.0.0.1"
   }
 }
}
```


