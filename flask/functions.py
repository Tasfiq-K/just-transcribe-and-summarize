import os
import requests
from flask import Flask, render_template, request
import torch
import whisperx
from transformers import pipeline
from pytube import YouTube
from pytube.exceptions import AgeRestrictedError

def predict_tags(input_text):
    response = requests.post("https://g0blas-paper-task-suggestion.hf.space/run/predict",
                             json={
                                 "data": [
                                     input_text
                                ]
                             }).json()
    data = response["data"]
    
    return data

def audio_to_text(url: str):
    """
    Args:
        link: [str] -> takes a youtube video link
    returns:
    """



    device = "cuda" if torch.cuda.is_available() else "cpu"
    bs = 16
    compute_type = "float16"
    
    f_name = 'audio_file.mp4' # the file name to save with
    yt = YouTube(url)

    # if GPU available run this block
    if device == 'cuda': 
        try:
            model = whisperx.load_model("large-v2", device, compute_type=compute_type)
            yt.streams.filter(only_audio=True)
            stream = yt.streams.get_by_itag(139)
            stream.download('', f_name)
            audio = whisperx.load_audio(f_name)
            result = model.transcribe(audio, batch_size=bs, language='en')
            res = [ i['text'] for i in result['segments'] ]
            os.remove(f"{f_name}")
            
            return res[0]
        
        except AgeRestrictedError:
            res = ""
            return res
    
    else:   # else run this block
        
        try:
            model = whisperx.load_model("large-v2", device, compute_type=compute_type)
            yt.streams.filter(only_audio=True)
            stream = yt.streams.get_by_itag(139)
            stream.download('', f_name)
            audio = whisperx.load_audio(f_name)
            result = model.transcribe(audio, language='en')
            res = [ i['text'] for i in result['segments'] ]
            os.remove(f"{f_name}")
            
            return res[0]
        
        except AgeRestrictedError:
            
            res = ""
            return res

