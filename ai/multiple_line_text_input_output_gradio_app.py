
from mlx_lm import load, generate

import gradio as gr

#model, tokenizer = load("mlx-community/sqlcoder-70b-alpha-4bit-mlx")
model, tokenizer = load("./")

def predict(text):
    response = generate(model, tokenizer, prompt=text, verbose=True)
    return response

demo = gr.Interface(
  fn=predict,
  inputs=[gr.Textbox(lines=10, placeholder="group order count by date for all orders. t_order: user, product_id, price, count, gmt_create, gmt_modified, status")],
  outputs=[gr.Textbox(lines=10)],
)

demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
