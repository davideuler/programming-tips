4090 因为显存不足，不能直接运行。 需要把 checkpoint 文件转换为 ft 版本。

前提条件：
已经下载好了 checkpoint 文件列表，并且合并后解压为 codegeex_13b.pt。


# 1.运行容器，进入到支持 GPU的 pytorch 环境，
```
git clone https://github.com/CodeGeeX/codegeex-fastertransformer
cd codegeex-fastertransformer
docker pull nvcr.io/nvidia/pytorch:21.11-py3
docker run -p 9114:5000 --cpus 28 --gpus all -it -v `pwd`:/workspace/codegeex-fastertransformer -v /data/workspace/:/data/workspace --ipc=host  --name=test nvcr.io/nvidia/pytorch:21.11-py3
```

如果启动容器时遇到这个错误： could not select device driver "" with capabilities: [[gpu]]

说明 nvidial 的驱动没有装好，需要在主机上安装驱动。 解决方法：
https://collabnix.com/introducing-new-docker-cli-api-support-for-nvidia-gpus-under-docker-engine-19-03-0-beta-release/

https://github.com/NVIDIA/nvidia-docker/issues/1034

# 2.容器中运行脚本 make_all.sh 生成 ft 版本 checkpoint 文件
link make to gmake:

```
ln -s /usr/bin/make /usr/bin/gmake

pip3 install transformers -i https://mirror.baidu.com/pypi/simple
pip3 install sentencepiece -i https://mirror.baidu.com/pypi/simple
pip install fire -i https://mirror.baidu.com/pypi/simple
cd codegeex-fastertransformer
sh make_all.sh 
```

# 3.更新容器中 get_ckpt_ft.py 脚本里面的 pt 文件路径。运行脚本：

运行 python get_ckpt_ft.py 生成 ft 版本 ckpt.

# 4.容器中启动服务：
```
python3 api.py --data_type int8 --ckpt_path /data/workspace/CodeGeeX/codegeex_13b_ft.pt
```

# 5.运行测试：
python3 post.py

也可以更改 post.py, 从宿主机调用本机的 9114 端口来提交数据。

效果示例：
<img width="1475" alt="image" src="https://user-images.githubusercontent.com/377983/228922839-bbf8d3c0-8d33-4053-bc71-3c261192bfc6.png">
