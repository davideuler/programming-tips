# MoonCast: High-Quality Zero-Shot Podcast Generation
# https://github.com/jzq2000/MoonCast
# mount models to /app/resource for container running

FROM pytorch/pytorch:2.3.1-cuda12.1-cudnn8-devel

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV GRADIO_SERVER_NAME=0.0.0.0
ENV GRADIO_SERVER_PORT=7860

# Install system dependencies
ENV TZ=Asia/Shanghai PIP_INDEX_URL=http://mirrors.cloud.aliyuncs.com/pypi/simple/ PIP_TRUSTED_HOST=mirrors.cloud.aliyuncs.com

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    git \
    wget \
    curl \
    ffmpeg \
    libsndfile1 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt
# RUN pip install flash-attn --no-build-isolation

RUN pip install https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/download/v0.0.4/flash_attn-2.7.3+cu121torch2.3-cp310-cp310-linux_x86_64.whl
RUN pip install huggingface_hub
RUN pip install gradio==5.22.0
RUN pip install pydub

# Copy application code
COPY . .

# Expose port
EXPOSE 7860

# Run the application
CMD ["python", "app.py"]
