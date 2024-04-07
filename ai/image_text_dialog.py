# pip install gradio==3.50
import gradio as gr
from PIL import Image
from torchvision.transforms import Resize
from torchvision.transforms.functional import pil_to_tensor
import torch
from moai.load_moai import prepare_moai

# Assuming the moai setup and processing code is in a file named moai_utils.py
# from moai_utils import prepare_moai, process_image_and_prompt

# Load MoAI models and processors
moai_model, moai_processor, seg_model, seg_processor, od_model, od_processor, sgg_model, ocr_model = prepare_moai(moai_path='BK-Lee/MoAI-7B', bits=4, grad_ckpt=False, lora=False, dtype='fp16')

def process_image_and_prompt(image, prompt):
    # Pre-processing for MoAI
    image_tensor = Resize(size=(490, 490), antialias=False)(pil_to_tensor(image))
    moai_inputs = moai_model.demo_process(image=image_tensor,
                                        prompt=prompt,
                                        processor=moai_processor,
                                        seg_model=seg_model,
                                        seg_processor=seg_processor,
                                        od_model=od_model,
                                        od_processor=od_processor,
                                        sgg_model=sgg_model,
                                        ocr_model=ocr_model,
                                        device='cuda:0')

    # Generate
    with torch.inference_mode():
        generate_ids = moai_model.generate(**moai_inputs, do_sample=True, temperature=0.9, top_p=0.95, max_new_tokens=256, use_cache=True)

    # Decoding
    answer = moai_processor.batch_decode(generate_ids, skip_special_tokens=True)[0].split('[U')[0]
    return answer

# Create Gradio interface
iface = gr.Interface(fn=process_image_and_prompt,
                     inputs=[gr.inputs.Image(type="pil", label="Upload Image"),
                             gr.Textbox(lines=2, placeholder="Enter your prompt here...", label="Prompt")],
                     outputs=[gr.Textbox(lines=5, label = "Response")],
                     title="Image Description Generator",
                     description="Upload an image and enter a prompt to get a detailed description.")

# [3] Launch the application
iface.launch(server_name="0.0.0.0", server_port=7860)
