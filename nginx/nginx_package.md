

// 指明需要http2模块, sub module 模块（支持 proxy 页面的内容过滤）
tar zxvf tengine-2.3.3.tar.gz
cd tengine-2.3.3
./configure --prefix=/data/tengine --with-http_realip_module  --with-http_gzip_static_module  --with-http_v2_module --with-http_sub_module --with-pcre=/data/pcre-8.44
make -j16
make install
