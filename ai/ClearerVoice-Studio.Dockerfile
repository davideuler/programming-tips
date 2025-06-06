# Dockerfile for ClearerVoice-Studio
# When running the container, mount a checkpoint folder to /app/models

FROM pytorch/pytorch:2.4.1-cuda12.1-cudnn9-runtime

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV GRADIO_SERVER_NAME=0.0.0.0

# Install system dependencies
ENV TZ=Asia/Shanghai PIP_INDEX_URL=http://mirrors.cloud.aliyuncs.com/pypi/simple/ PIP_TRUSTED_HOST=mirrors.cloud.aliyuncs.com

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    ffmpeg \
    git \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

# Install streamlit
RUN pip install streamlit

# Copy project files
COPY . .


# Install clearvoice package
RUN cd clearvoice && pip install -e .

# Create necessary directories
RUN mkdir -p temp

# Expose port for Streamlit
EXPOSE 8501

# Set the command to run Streamlit app
CMD ["streamlit", "run", "clearvoice/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
