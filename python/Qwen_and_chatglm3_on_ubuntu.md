# Qwen and ChatGLM3 on ubuntu 20.04

## 1.通义千问安装

### 环境
Ubuntu 22.04,  python 3.10,  torch==2.0.1 , cuda 11.4

### 参考

* https://www.modelscope.cn/models/qwen/Qwen-14B-Chat/summary
* https://github.com/QwenLM/Qwen

### 安装千问：

```
  python3.10 -m venv llmenv
  source llmenv/bin/activate
  pip install --upgrade pip
  pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2
  git clone https://github.com/QwenLM/Qwen
  cd Qwen
  pip install -r requirements.txt

  pip install modelscope mdtex2html gradio  optimum auto-gptq

```

### 运行服务

创建  run_qwen.py 文件,    vim run_qwen.py
```
from modelscope import AutoModelForCausalLM, AutoTokenizer, snapshot_download
from modelscope import GenerationConfig

model_dir = snapshot_download('Qwen/Qwen-14B-Chat', revision='v1.0.4')

# Note: The default behavior now has injection attack prevention off.
tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)

# use bf16
# model = AutoModelForCausalLM.from_pretrained(model_dir, device_map="auto", trust_remote_code=True, bf16=True).eval()
# use cpu only
# model = AutoModelForCausalLM.from_pretrained(model_dir, device_map="cpu", trust_remote_code=True).eval()
# use auto mode, automatically select precision based on the device.
model = AutoModelForCausalLM.from_pretrained(model_dir, device_map="auto", trust_remote_code=True).eval()

# Specify hyperparameters for generation
model.generation_config = GenerationConfig.from_pretrained(model_dir, trust_remote_code=True) # 可指定不同的生成长度、top_p等相关超参

# 第一轮对话 1st dialogue turn
response, history = model.chat(tokenizer, "你好", history=None)
print(response)
# 你好！很高兴为你提供帮助。

# 第二轮对话 2nd dialogue turn
response, history = model.chat(tokenizer, "给我讲一个年轻人奋斗创业最终取得成功的故事。", history=history)
print(response)
```

运行 run_qwen.py 下来模型，然后链接模型到当前目录 :
```
ln -s ~/.cache/modelscope/hub/Qwen Qwen
python web_demo.py
```

详细环境：
NVIDIA-SMI 470.82.01    Driver Version: 470.82.01    CUDA Version: 11.4
Python 3.10.8,  Ubuntu, 20.04.6 LTS (Focal Fossa), torch.__version__  = 2.0.1+cu117
Nvidia V100x8

显存要求：
Qwen-14B-Chat 2048 context: 30.15GB
Qwen-14B-Chat-Int4 2048 context:  13.00GB

注意：
这个环境中，Qwen-7B-Chat 跑不起来（需要 flash attention,  安装时 RuntimeError: FlashAttention is only supported on CUDA 11.6 and above.）。
同时 Qwen-7B-Chat-Int4 跑不起来，运行时 auto-gptq 出错（不兼容 cuda 11.x）。

### Flask api service for Qwen:

```
# chat_api.py
from modelscope import AutoModelForCausalLM, AutoTokenizer, snapshot_download
from modelscope import GenerationConfig

from flask import Flask, request, jsonify

app = Flask(__name__)
model_dir = snapshot_download('Qwen/Qwen-14B-Chat', revision='v1.0.4')
print("initializing model....")

# Note: The default behavior now has injection attack prevention off.
tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)

# use bf16
# model = AutoModelForCausalLM.from_pretrained(model_dir, device_map="auto", trust_remote_code=True, bf16=True).eval()
# use cpu only
# model = AutoModelForCausalLM.from_pretrained(model_dir, device_map="cpu", trust_remote_code=True).eval()
# use auto mode, automatically select precision based on the device.
model = AutoModelForCausalLM.from_pretrained(model_dir, device_map="auto", trust_remote_code=True).eval()
model.generation_config = GenerationConfig.from_pretrained(model_dir, trust_remote_code=True) # 可指定不同的生成长度、top_p等相关超参

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data['message']
    history = data['history']
    response, history = model.chat(tokenizer, message, history=None)

    return jsonify({'response': response, 'history': history})

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Flask Chat API')
    parser.add_argument('--host', default='127.0.0.1', help='Hostname (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=5000, help='Port (default: 5000)')
    args = parser.parse_args()

    app.run(host=args.host, port=args.port, debug=True, use_reloader=False)
```

Start the service:
```
pip install flask
python chat_api.py --host 0.0.0.0 --port 8080
```

## 2.ChatGLM3 服务 & API

https://modelscope.cn/models/ZhipuAI/chatglm3-6b/summary

### Run ChatGLM3 Rest Service by Flask

```python
# chat_api.py
from flask import Flask, request, jsonify
app = Flask(__name__)

from modelscope import AutoTokenizer, AutoModel, snapshot_download
model_dir = snapshot_download("ZhipuAI/chatglm3-6b", revision = "v1.0.0")
tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)
model = AutoModel.from_pretrained(model_dir, trust_remote_code=True).half().cuda()
model = model.eval()

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data['message']
    history = data['history']
    response, history = model.chat(tokenizer, message, history=None)

    return jsonify({'response': response, 'history': history})


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Flask Chat API')
    parser.add_argument('--host', default='127.0.0.1', help='Hostname (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=5000, help='Port (default: 5000)')
    args = parser.parse_args()

    app.run(host=args.host, port=args.port, debug=True, use_reloader=False)

#response, history = model.chat(tokenizer, "你好", history=[])
#print(response)
```

Start the server:
```
pip install flask
python chat_api.py --host 0.0.0.0 --port 8080
```

### 客户端调用

``` python
import requests

modelscope_chat_url = "http://127.0.0.1:8080/api/chat"  # chatglm3b service

def chat_chatglm(prompt, history=[]):
    url = modelscope_chat_url

    # Create the request payload
    payload = {
        "message": prompt,
        "history": history
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an exception if the request was not successful
        result = response.json() #  return history, response
        return result
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

print(chat_chatglm("hello"))
```

## FAQs

Pip package for pytorch which works with Cuda
Pytorch 与 Cuda 的版本兼容列表：

https://pytorch.org/get-started/previous-versions/

Q1: cuda 11.4 的驱动（nvidia-smi看到的版本号）， 如何安装 torch ?
A: cuda 11.4/11.6 的驱动，可以使用 torch cu113, cu118 兼容的 pip 包, 详细讨论:
pytorch/pytorch#75992

pip install torch==1.12.1+cu113 torchvision==0.13.1+cu113 torchaudio==0.12.1 --extra-index-url https://download.pytorch.org/whl/cu113

可以从镜像站下载包安装, 搭配 Python 3.10 的版本包：
wget https://mirror.sjtu.edu.cn/pytorch-wheels/cu113/torch-1.12.0+cu113-cp310-cp310-linux_x86_64.whl

Q2: 只有 cuda 11.4 的系统驱动(nvidia-smi)， 要使用 torch 2.0.1 以上的版本，如何安装 torch?
A: 如果需要使用 torch 2.0.1 以上的版本，但 ubuntu 系统只有 cuda 11.4 的驱动，可以使用 torch 2.0.1 & cu11 的编译版本：
pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cu118

参考：https://discuss.pytorch.org/t/which-pytorch-version-2-0-1-support-cuda-11-4/190446/3
