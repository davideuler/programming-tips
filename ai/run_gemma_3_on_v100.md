
Dockerfile

```
FROM vllm/vllm-openai:v0.8.5

WORKDIR /app

# Set environment variables
ENV GRADIO_SERVER_NAME=0.0.0.0
ENV HF_HOME=/root/.cache/huggingface

# Create cache directory
ENV TZ=Asia/Shanghai PIP_INDEX_URL=https://mirrors.sustech.edu.cn/pypi/web/simple PIP_TRUSTED_HOST=mirrors.sustech.edu.cn

RUN mkdir -p /root/.cache/huggingface

# Expose port
EXPOSE 8000

# Set entrypoint and command
ENTRYPOINT ["vllm"]

CMD ["serve", "google/gemma-3-1b-it", "--max-model-len", "8192", "--port", "8000", "--dtype", "float32"]
```

vllm v0.8.5 support running on V100. Newer vllm like v0.9.0 works for later GPUs.
