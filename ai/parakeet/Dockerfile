# parakeet-tdt-0.6b-v2
FROM nvcr.io/nvidia/pytorch:24.07-py3

# Ensure apt-get won't prompt for selecting options
ENV DEBIAN_FRONTEND=noninteractive

# libavdevice-dev required for latest torchaudio
RUN apt-get update && \
  apt-get upgrade -y && \
  apt-get install -y \
  libsndfile1 sox \
  libfreetype6 \
  libsox-fmt-all \
  swig \
  ffmpeg \
  libavdevice-dev && \
  rm -rf /var/lib/apt/lists/*

ENV GRADIO_SERVER_NAME=0.0.0.0

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip setuptools wheel && \
    pip install gradio==3.50.2 nemo_toolkit[asr] 

RUN pip install numpy

EXPOSE 7860

CMD ["python", "gradio_app.py"]
