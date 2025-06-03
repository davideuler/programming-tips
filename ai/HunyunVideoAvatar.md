
Failed to run by OOM on A100. Smaller image resolution may be supported.

Dockerfile:
```
FROM nvidia/cuda:12.6.0-cudnn-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

ENV TZ=Asia/Shanghai PIP_INDEX_URL=http://mirrors.cloud.aliyuncs.com/pypi/simple/ PIP_TRUSTED_HOST=mirrors.cloud.aliyuncs.com

RUN apt-get update && apt-get install -y git ffmpeg libgl1 python3 python3-pip && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt
RUN pip install ninja
#RUN pip install git+https://github.com/Dao-AILab/flash-attention.git@v2.6.3
#RUN pip install flash-attn==2.6.3 --no-build-isolation
RUN pip install https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/download/v0.0.8/flash_attn-2.6.3+cu126torch2.6-cp310-cp310-linux_x86_64.whl
RUN pip install torch==2.6.0 torchvision
RUN pip install pydantic==2.10.6

ENV GRADIO_SERVER_NAME=0.0.0.0

EXPOSE 7860
RUN chmod +x monkey_patch.py && python monkey_patch.py hymm_gradio/gradio_audio.py || python3 monkey_patch.py hymm_gradio/gradio_audio.py
CMD ["bash", "single_gpu_gradio.sh"]
```

single_gpu_gradio.sh

```
#!/bin/bash
JOBS_DIR=$(dirname $(dirname "$0"))
export PYTHONPATH=./

export MODEL_BASE=./weights
OUTPUT_BASEPATH=./results-single

checkpoint_path=${MODEL_BASE}/ckpts/hunyuan-video-t2v-720p/transformers/mp_rank_00_model_states_fp8.pt

export DISABLE_SP=1 
CUDA_VISIBLE_DEVICES=0 python3 hymm_sp/sample_gpu_poor.py \
    --input 'assets/test.csv' \
    --ckpt ${checkpoint_path} \
    --sample-n-frames 129 \
    --seed 128 \
    --image-size 704 \
    --cfg-scale 7.5 \
    --infer-steps 50 \
    --use-deepcache 1 \
    --flow-shift-eval-video 5.0 \
    --save-path ${OUTPUT_BASEPATH} \
    --use-fp8 \
    --infer-min &


python3 hymm_gradio/gradio_audio.py
```

docker-compose
```
services:
  hunyuanvideo:
    build:
      context: .
      dockerfile: Dockerfile
    image: exp-hunyuanvideo
    container_name: exp-hunyuanvideo
    ports:
      - "${MAPPED_HOST_PORT_HUNYUANVIDEO}:7860"
    environment:
      - GRADIO_SERVER_NAME=0.0.0.0
    volumes:
      - ~/models/${PROJECT_ADDRESS}/weights:/app/weights
      - ~/.cache:/root/.cache
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    networks:
      - hunyuan_net

networks:
  hunyuan_net:
    driver: bridge
```

Download weights before run the app:
```
cd weights/
pip install "huggingface_hub[cli]"
cd weights && huggingface-cli download tencent/HunyuanVideo-Avatar --local-dir ./
```
