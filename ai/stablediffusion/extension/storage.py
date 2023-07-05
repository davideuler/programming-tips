
import base64, uuid
from io import BytesIO
import os,json
import re
import modules.scripts as scripts
import gradio as gr

from init_ots_table import create_table, insert_row
from oss_util import upload_to_oss, upload_bytes_to_oss
from config import PK, USER_ID, WORKSPACE_ID


pk, user_id, workspace_id = PK, USER_ID, WORKSPACE_ID

#create_table_if_not_exist()

class Scripts(scripts.Script):
    def title(self):
        return "Cloud Storage"

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
      
        return []

    def split_key_value(self, text):
        pos = text.index(": ")
        return (text[:pos], text[pos+2:])

    def postprocess(self, p, processed):
        # Extract image information
        regex = r"Steps:.*$"
        info = re.findall(regex, processed.info, re.M)[0]
        # Steps: 20, Sampler: Euler a, CFG scale: 7, Seed: 59944576, Size: 512x512, Model hash: ef49fbb25f, Model: AnyLoRA, Lora hashes: "大月阿露露_base_loraYabuki: e96f805afa76", Version: v1.4.0
        input_dict = dict( self.split_key_value(item) for item in str(info).split(", "))
        steps = int(input_dict["Steps"])
        seed = int(input_dict["Seed"])
        sampler = input_dict["Sampler"]
        cfg_scale = float(input_dict["CFG scale"])
        size = tuple(map(int, input_dict["Size"].split("x")))
        model_hash = input_dict["Model hash"]
        model = input_dict["Model"]
        lora_hash = input_dict.get("Lora hashes")
            
        record_id = str(uuid.uuid4())
        image_list = []
        
        for i in range(len(processed.images)):
            seed = processed.seed
            prompt = processed.prompt
            neg_prompt = processed.negative_prompt


            image = processed.images[i] # PIL.Image
            buffer = BytesIO()
            image.save(buffer, "png")
            image_bytes = buffer.getvalue()
            
            oss_file_name = f"sd_images/{user_id}/{workspace_id}/{record_id}/{i}.png"
            
            upload_bytes_to_oss(image_bytes, oss_file_name)
            image_list.append(oss_file_name)

        parameters = {
                "prompt": prompt, 
                "negative_prompt": neg_prompt, 
                "steps": int(steps), 
                "seed": int(seed), 
                "sampler": sampler,
                "cfg_scale": float(cfg_scale), 
                "size": size, 
                "model_hash": model_hash, 
                "model": model,
                "lora_hash":lora_hash
        }
        
        print("insert result of record_id: ", record_id, pk, user_id, workspace_id, prompt, ','.join(image_list) , parameters)
        insert_row(pk, user_id, workspace_id, record_id, prompt,  json.dumps(image_list, ensure_ascii=False), model_name = model, request_params=json.dumps(parameters, ensure_ascii=False))
        return True
