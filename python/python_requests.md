
## When request a remote service through proxy like 127.0.0.1:1080, and got error like this:

```
Max retries exceeded with url: /api/conversation (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1123)')))
```

Then can bypass the SSL verification of the proxy when requesting the service.

```
  requests.get('https://example.com', verify=False) 
```

or set the verify property of Session to False if use a Session.

```
  self.session = requests.Session() 
  self.session.verify = False
```
