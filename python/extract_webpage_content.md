
# see
 https://github.com/currentslab/extractnet
 https://github.com/currentslab/extractnet/issues/12

# pip requirements

```
 pip install extractnet -i https://mirror.baidu.com/pypi/simple
 pip uninstall regex -y
 pip install regex==2022.3.2 -i https://mirror.baidu.com/pypi/simple
```

example code

```
import requests
from extractnet import Extractor

agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"

headers = {'User-Agent': agent}
def extract_content_from_url(url:str):
    raw_html = requests.get(url, headers=headers).text
    results = Extractor().extract(raw_html)
    return results.get("title"), results.get("content")

def extract_content_from_html(raw_html):
    results = Extractor().extract(raw_html)
    return results.get("title"), results.get("content")
    
```
