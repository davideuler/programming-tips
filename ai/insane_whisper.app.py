#!/bin/env python
import os,time
import torch
from transformers import pipeline

from werkzeug.utils import secure_filename
from threading import Thread

import gradio as gr
from flask import Flask, request, jsonify

model_name = "openai/whisper-large-v3"
model_name = "openai/whisper-small"
pipe = pipeline(
    "automatic-speech-recognition",
    model=model_name,
    torch_dtype=torch.float16,
    device="cuda", # or mps for Mac devices
    model_kwargs={"use_flash_attention_2": True}, # set to False for old GPUs
)

#pipe.model = pipe.model.to_bettertransformer() # only if `use_flash_attention_2` is set to False

def timeit(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        elapsed = end - start
        print(f'Time taken: {elapsed:.6f} seconds')
        return result
    return wrapper


@timeit
def predict(file_name = "/home/david/Israel_and_Palestine.mp3"):
    outputs = pipe(file_name, chunk_length_s=30, batch_size=24, return_timestamps=True)
    return outputs

# Gradio Application
@timeit
def transcribe_audio(file_path, task):
    print("transcribing audio file:%s task:%s" % (file_path, task))
    outputs = pipe(file_path, chunk_length_s=30, batch_size=24, return_timestamps=True)
    #transcription = " ".join([chunk["text"] for chunk in outputs])
    #print("transcribed text:%s %s" % (type(outputs), outputs))
    return outputs["text"], file_path


# Create the Gradio interface
#inputs = gr.inputs.Audio(source="upload", type="filepath", label="Upload Audio File")
inputs = [
    gr.Audio(source="upload", type="filepath", label="Upload Audio File"),
    gr.Radio(["transcribe", "translation"], default="transcribe", label="Task")
]
t1 = gr.Textbox(label="Output")
t2 = gr.Textbox(label="Uploaded File Name"),

# Launch the Gradio app
def run_gradio():
    gr.Interface(fn=transcribe_audio, inputs=inputs, outputs=["text", "text"], title="Audio Transcription").launch(server_name="0.0.0.0", server_port=8002)

# Flask API
app = Flask(__name__)

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join('/tmp', filename)
        file.save(file_path)
        try:
            transcription_output = transcribe_audio(file_path)
            transcription = " ".join([chunk["text"] for chunk in transcription_output])
            return jsonify({'transcription': transcription})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)

def run_flask(args):
    app.run(host=args.host, port=args.port, debug=True, use_reloader=False)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Flask Chat API')
    parser.add_argument('--host', default='127.0.0.1', help='Hostname (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=5000, help='Port (default: 5000)')
    args = parser.parse_args()

    # Run Flask in a separate thread
    flask_thread = Thread(target=run_flask, args=(args,))
    flask_thread.start()

    run_gradio()

