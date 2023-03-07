
## Docker desktop need a HTTP proxy to pull image from Docker hub.

And I need to convert my local socks5 proxy to http.

### Options:
https://github.com/KaranGauswami/socks-to-http-proxy

https://github.com/oyyd/http-proxy-to-socks

https://github.com/qwj/python-proxy

### Example to 

```
wget https://github.com/KaranGauswami/socks-to-http-proxy/releases/download/v0.3.0/sthp-macos
chmod +x sthp-macos
sthp -p 8080 -s 127.0.0.1:1080
# This will create proxy server on 8080 and use localhost:1080 as a Socks5 Proxy


```
