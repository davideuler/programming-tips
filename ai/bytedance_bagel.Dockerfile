# ByteDance BAGEL
# Mount the models to /app/models for container to run (avoid duplicate downloading of models)
FROM pytorch/pytorch:2.7.0-cuda12.6-cudnn9-runtime

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV GRADIO_SERVER_NAME=0.0.0.0
ENV GRADIO_SERVER_PORT=7860

# Install system dependencies
#ENV TZ=Asia/Shanghai PIP_INDEX_URL=http://mirrors.cloud.aliyuncs.com/pypi/simple/ PIP_TRUSTED_HOST=mirrors.cloud.aliyuncs.com

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    git \
    wget \
    curl libgl1 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

RUN pip install torch==2.7.0 torchvision torchaudio==2.7.0  --index-url https://download.pytorch.org/whl/cu126 --force-reinstall
RUN pip install https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/download/v0.0.8/flash_attn-2.7.4.post1+cu126torch2.7-cp311-cp311-linux_x86_64.whl
RUN pip uninstall -y opencv-python numpy scipy && pip install opencv-python-headless numpy scipy

# Copy the entire project
COPY . .

# Create models directory
RUN mkdir -p models

# Expose port
EXPOSE 7860

# Default command to run the Gradio app
CMD ["python", "app.py", "--server_name", "0.0.0.0", "--server_port", "7860", "--mode", "2"]
