
https://gist.github.com/evantoli/f8c23a37eb3558ab8765

```
git config --global http.proxy http://127.0.0.1:1090
```

Consider something like:

```
git config --global http.proxy http://proxyUsername:proxyPassword@proxy.server.com:port
```

Or for a specific domain, something like:

```
git config --global http.https://domain.com.proxy http://proxyUsername:proxyPassword@proxy.server.com:port
git config --global http.https://domain.com.sslVerify false
```

Setting http.<url>.sslVerify to false may help you quickly get going if your workplace employs man-in-the-middle HTTPS proxying. Longer term, you could get the root CA that they are applying to the certificate chain and specify it with either http.sslCAInfo or http.sslCAPath.

