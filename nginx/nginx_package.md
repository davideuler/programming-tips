

##  指明需要http2模块, sub module 模块（支持 proxy 页面的内容过滤）
tar zxvf tengine-2.3.3.tar.gz
cd tengine-2.3.3
./configure --prefix=/data/tengine --with-http_realip_module  --with-http_gzip_static_module  --with-http_v2_module --with-http_sub_module --with-pcre=/data/pcre-8.44
make -j16
make install


## Config proxy pass and proxy cache for pages (proxy pass all traffic of new.mydomain.com to origin.com)

https://stackoverflow.com/questions/5100883/why-nginx-does-not-cache-my-content
https://serverfault.com/questions/487104/nginx-not-caching-pages-immediately
http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_ignore_headers

set cache in http part of nginx.conf

```
http {
    include       mime.types;
    default_type  application/octet-stream;
    charset utf-8;
    
    client_header_timeout 600s;
    client_body_timeout 600s;
    client_max_body_size 20m;    #允许上传的最大文件大小
    proxy_cache_path /data/tengine/cache/origin keys_zone=mycache:50m max_size=3000m inactive=9256000m;
    ## ......
}
```

Then enable cache in the server configuration as follows.

```

server {
    listen 443 ssl;
    listen [::]:443 ssl;

     server_name  new.mydomain.cn;

     proxy_cache mycache;

     location / {
      proxy_set_header Accept-Encoding "";
      sub_filter_once off;
      sub_filter_types *;
#      sub_filter 'https:' 'http:';

      sub_filter "origin.com"  "new.mydomain.com";
      proxy_pass https://origin.com/;

      # make cache works:
      # proxy_cache_key $scheme://$host$uri$is_args$query_string;
      proxy_cache_key $request_uri;
      proxy_buffering on;
      proxy_cache_valid any 98000h;
      expires 48h;
      # https://serverfault.com/questions/487104/nginx-not-caching-pages-immediately
      # http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_ignore_headers
      proxy_ignore_headers Set-Cookie;
      proxy_ignore_headers Expires;
      proxy_hide_header Set-Cookie;

        #    proxy_redirect off; ## proxy redirect for 301 location redirect
        proxy_redirect https://origin.com/ /;
         proxy_set_header Host origin.com;
         proxy_set_header X-Real-IP $remote_addr;
         proxy_set_header REMOTE-HOST $remote_addr;
         proxy_connect_timeout 300;

         #后端服务器回传时间，就是在规定时间内后端服务器必须传完所有数据
         proxy_send_timeout 300;

         #连接成功后等待后端服务器的响应时间，已经进入后端的排队之中等候处理
         proxy_read_timeout 600;

         proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504 http_403 http_404;
    }
```
