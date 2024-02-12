
## Run llm inference on cpu by Pytorch

https://github.com/llSourcell/DoctorGPT

```python
# run.py
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    HfArgumentParser,
    AutoTokenizer,
    TrainingArguments,
)

model_path = "./medllama2_7b"


tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_path, trust_remote_code=True).cpu()

#inputs = tokenizer("幽门杆菌如何治疗?", return_tensors="pt")
inputs = tokenizer("How to deal with toothache?", return_tensors="pt")
outputs = model.generate(**inputs, max_length=512)
print(tokenizer.batch_decode(outputs, skip_special_tokens=True))
```

## Run GPU inference on Mac M1 by Pytorch and MPS
```python
# run.mps.py
import torch

from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    HfArgumentParser,
    AutoTokenizer,
    TrainingArguments,
)

model_path = "./medllama2_7b"

mps_device = torch.device("mps")


tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_path, trust_remote_code=True) #.cpu()

model.to(mps_device)

#inputs = tokenizer("幽门杆菌如何治疗?", return_tensors="pt")
inputs = tokenizer("How to deal with toothache?", return_tensors="pt").to(mps_device)
outputs = model.generate(**inputs, max_length=512,) # temperature=0.2, do_sample=True,
print(tokenizer.batch_decode(outputs, skip_special_tokens=True))
```

## Run GPU inference on Mac M1 by CPU, another example

```python
# run.py
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import math

## v2 models
model_path = "cloudyu/Mixtral_11Bx2_MoE_19B"

tokenizer = AutoTokenizer.from_pretrained(model_path, use_default_system_prompt=False, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch.float32, device_map='cpu', local_files_only=False, trust_remote_code=True).half()

print(model)
prompt = "hello world in Python:"
while not "q" == prompt:
  if len(prompt) == 0:
      prompt = input("please input prompt(q to quit):")
      continue
  print("input:%s\n" % prompt)
  input_ids = tokenizer(prompt, return_tensors="pt").input_ids

  generation_output = model.generate(input_ids=input_ids, max_new_tokens=500,repetition_penalty=1.2)
  print(tokenizer.decode(generation_output[0], skip_special_tokens=True))
  prompt = input("please input prompt(q to quit):")
```