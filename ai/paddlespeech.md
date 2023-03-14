
## Install paddlepaddle

### Dependency Introduction
gcc >= 4.8.5
paddlepaddle >= 2.4.1
python >= 3.7
OS support: Linux(recommend), Windows, Mac OSX


```
pip install paddlepaddle -i https://mirror.baidu.com/pypi/simple

```

## Install paddlespeech


pip install pytest-runner -i https://mirror.baidu.com/pypi/simple
pip install paddlespeech -i https://mirror.baidu.com/pypi/simple


## Speech Recognition

wget -c https://paddlespeech.bj.bcebos.com/PaddleAudio/zh.wav
wget -c https://paddlespeech.bj.bcebos.com/PaddleAudio/en.wav

paddlespeech asr --lang zh --input zh.wav

Python API example

```
>>> from paddlespeech.cli.asr.infer import ASRExecutor
>>> asr = ASRExecutor()
>>> result = asr(audio_file="zh.wav")
>>> print(result)
我认为跑步最重要的就是给我带来了身体健康
```

## TTS Text-to-Speech
Open Source Speech Synthesis, Output 24k sample rate wav format audio

command line experience

```
paddlespeech tts --input "你好，欢迎使用百度飞桨深度学习框架！" --output output.wav

paddlespeech tts --input "欢迎和我一起学习 Python 编程，这是一个有趣的编程语言！" --am fastspeech2_csmsc --voc mb_melgan_csmsc --output fastspeech_mb_melgan_csmsc.wav

paddlespeech tts --input "欢迎和我一起学习 Python 编程，这是一个有趣的编程语言！" --am fastspeech2_csmsc --voc hifigan_csmsc --output fastspeech2_hifigan_csmsc.wav

# hifigan_vctk is for English
paddlespeech tts --input "欢迎和我一起学习 Python 编程，这是一个有趣的编程语言！" --am fastspeech2_male --voc hifigan_male  --output hifigan_male.wav

paddlespeech tts --input "欢迎和我一起学习 Python 编程，这是一个有趣的编程语言！" --am fastspeech2_male --voc mb_melgan_csmsc --output mb_melgan_csmsc.wav

paddlespeech tts --input "欢迎和我一起学习 Python 编程，这是一个有趣的编程语言！" --am speedyspeech_csmsc --voc pwgan_male --output pwgan_male.wav

```

Python API 

```
>>> from paddlespeech.cli.tts.infer import TTSExecutor
>>> tts = TTSExecutor()
>>> tts(text="今天天气十分不错。", output="output.wav")
```

```
from paddlespeech.cli.tts.infer import TTSExecutor
tts = TTSExecutor()

##  FIXME: 指定 am, voc 没有效果
tts(text="今天天气十分不错。", am="fastspeech2_csmsc", voc="mb_melgan_csmsc",  output="fastspeech2_csmsc.wav", )
tts(text="今天天气十分不错。", am="fastspeech2_csmsc", voc="hifigan_male", output="fastspeech2_hifigan_male.wav",)

tts(text="今天天气十分不错。", am="fastspeech2_male", voc="hifigan_male", output="fastspeech2_male_hifigan.wav",)
tts(text="今天天气十分不错。", am="fastspeech2_male", voc="mb_melgan_csmsc", output="fastspemb_melgan.wav",)

#tts(text="今天天气十分不错。", am="speedyspeech_csmsc", voc="pwgan_male", output="speedyspeech_csmsc_pwgan_male.wav", )
#tts(text="今天天气十分不错。", am="speedyspeech_csmsc", voc="hifigan_male", output="speedyspeech_csmsc_hifigan_male.wav",)


```

## If got this error, python setup.py egg_info did not run successfully error: metadata-generation-failed, 

Check there is proper config in file ~/.pip/pip.conf, and ~/.pydistutils.cfg, remove all index-url config.

