Besides the pretrained models, also the spk2info should be prepared for CosyVoice2-0.5B. Howver the CosyVoice-300M-SFT works out-of-box.

## fastapi/server.py, KeyError: '中文女', could not found spk2info, 
https://github.com/FunAudioLLM/CosyVoice/issues/984

YI dict_keys(['中文女', '中文男', '日语男', '粤语女', '英文女', '英文男', '韩语女'])
I change the model from ’CosyVoice-300M‘ to ’CosyVoice-300M-SFT‘ in file runtime/python/fastapi/server.py, and the keyerror is addressed.

or start the fastapi server as:
/bin/bash -c "mkdir -p pretrained_models && cd /workspace/CosyVoice/runtime/python/fastapi && python3 server.py --port 50000 --model_dir iic/CosyVoice-300M-SFT  && sleep infinity"

## Another option
Copy a working spk2info.zip, decompress the file, copy the spk2info.pt to CosyVoice\runtime\python\fastapi.

And Start the application as:
python server.py --port 50000 --model_dir E:\sensevoice\CosyVoice\models\CosyVoice2-0.5B --spk_info spk2info.pt

Reference: https://blog.csdn.net/chui_yu666/article/details/147131301
