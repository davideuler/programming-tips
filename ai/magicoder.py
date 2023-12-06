#!/bin/env python

# after downloaded the Magicoder model, could serve the application 
# download the magicoder model: git clone https://huggingface.co/ise-uiuc/Magicoder-S-DS-6.7B

import gradio as gr
from transformers import pipeline

pipe = pipeline("text-generation", model="Magicoder-S-DS-6.7B")

def predict(text):
  return pipe(text, max_new_tokens=1024)[0]["generated_text"]

demo = gr.Interface(
  fn=predict,
  inputs='text',
  outputs='text',
)

demo.launch(server_name="0.0.0.0", server_port=8002, share=False)


