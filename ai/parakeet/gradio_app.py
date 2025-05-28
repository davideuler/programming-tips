import gradio as gr
import nemo.collections.asr as nemo_asr
import os

asr_model = nemo_asr.models.ASRModel.from_pretrained(model_name="nvidia/parakeet-tdt-0.6b-v2")

def transcribe(audio):
    if isinstance(audio, tuple):
        audio = audio[0]  # gradio returns (filepath, sample_rate)
    result = asr_model.transcribe([audio])
    return result[0].text

demo = gr.Interface(
    fn=transcribe,
    inputs=gr.Audio(source="upload", type="filepath", label="Upload 16kHz WAV/FLAC Audio"),
    outputs=gr.Textbox(label="Transcription"),
    title="Parakeet TDT 0.6B V2 ASR",
    description="Upload a 16kHz mono WAV or FLAC file to transcribe using NVIDIA's Parakeet TDT 0.6B V2 model."
)

demo.launch(server_name="0.0.0.0", server_port=7860)
