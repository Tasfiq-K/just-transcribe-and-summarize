import os
import requests
# from flask import Flask, render_template, request
import torch
# import whisperx
from faster_whisper import WhisperModel
from transformers import pipeline
from pytube import YouTube
from pytube.exceptions import AgeRestrictedError
from keybert import KeyBERT
from moviepy.editor import VideoFileClip


def predict_tags(input_text):
    """
    Predicts the tags for this blog/text
    args:
        input_text: [str] Text data
    returns: tags with their probability score
    """
    response = requests.post("https://g0blas-blog-tags-classifier.hf.space/run/predict", json={"data": [input_text] }).json()
    data = response["data"]

    return data


def audio_to_text(url=None, audio_file=None, file_path=None):
    """
    Args:
        link: [str] -> takes a youtube video link
    returns: transcribed text from video 

    """
    print(f"{file_path}")
    print(url)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    bs = 16
    model_size = 'small'

    if url:

        f_name = 'audio_file.mp4' # the file name to save with
        yt = YouTube(url)

        # if GPU available run this block
        if device == 'cuda':
            compute_type = "float16"
            model = WhisperModel(model_size_or_path=model_size, device=device, compute_type=compute_type)
            try:
                yt.streams.filter(only_audio=True)
                stream = yt.streams.get_by_itag(139)
                stream.download(file_path, f_name)
                # audio = whisperx.load_audio(os.path.join(file_path, f_name))
                result, _ = model.transcribe(f"{file_path}/{f_name}", language='en')

                res, _ = [ i.text for i in result ]
                # os.remove(f"static/{f_name}")

                return res[0]

            except AgeRestrictedError:
                res = ""
                return res

        else:   # else (cpu) run this block

            compute_type = "int8"
            model = WhisperModel(model_size_or_path=model_size, device=device, compute_type=compute_type)

            try:
                yt.streams.filter(only_audio=True)
                stream = yt.streams.get_by_itag(139)
                print("dowload strat")
                stream.download(file_path, f_name)
                print(f"saved to {file_path}/{f_name}")
                print(f"{file_path}, {f_name}")
                # audio = whisperx.load_audio(f"{file_path}/{f_name}")
                print("audio loaded")
                result, _ = model.transcribe(f"{file_path}/{f_name}", language='en')
                print("finishied transcribing")
                res = [ i.text for i in result ]
                # os.remove(f"static/{f_name}")

                print("returnin results")

                return res[0]

            except AgeRestrictedError:

                res = ""
                return res

    elif audio_file:
        # so, It's already in the audio format
        if device == 'cuda':
            compute_type = "float16"
            model = WhisperModel(model_size_or_path=model_size, device=device, compute_type=compute_type)
            # audio = whisperx.load_audio(os.path.join(file_path, audio_file)) # load the audio file
            result, _ = model.transcribe(f"{file_path}/{f_name}", language='en')
            res = [ i.text for i in result ]
            # os.remove(os.path.join())
            return res[0]

        compute_type = "int8"
        model = WhisperModel(model_size_or_path=model_size, device=device, compute_type=compute_type)
        # audio = whisperx.load_audio(os.path.join(file_path, audio_file)) # load the audio file
        result = model.transcribe(f"{file_path}/{f_name}", language='en')
        res = [ i.text for i in result ]

    return res[0]


def summarizer(text):
    """
    A text summaraizer
    args: 
        text: text data
    returns: returns the summarized version of the given text
    """
    max_length = 100
    min_length = 20

    device = "cuda" if torch.cuda.is_available() else "cpu"
    summ_text = pipeline("summarization", model="pszemraj/led-large-book-summary", device=device)

    summary = summ_text(text, min_length=min_length, max_length=max_length)

    return summary[0][ 'summary_text' ]


def summarizer_v2(text):
    """
    A text summaraizer; version 2
    args: 
        text: text data
    returns: returns the summarized version of the given text
    """


    API_URL = "https://api-inference.huggingface.co/models/pszemraj/led-large-book-summary"
    headers = {"Authorization": "Bearer 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"}

    response = requests.post(API_URL, headers=headers, json=text)
    res = response.json()

    return res


def keyword_extractor(text):
    """
    Extract keywords from the given text
    args: 
        text: Text data
    returns: String of top 5 keywords
    """
    top_kw = ""
    kw_model = KeyBERT()
    keywords = kw_model.extract_keywords(text, top_n=5)
    kws = [ i[0].title() for i in keywords ]
    top_kw = ", ".join(kws)

    return top_kw


def media_to_audio(media_file, file_path, output_ext="mp4", output_file="audio"):
    """
    converts media files like MP4, MOV, WMV, FLV, AVI, AVCHD, WebM, MKV into an MP4 audio file
    args: 
        media_file: [str]: name of the media file
        output_ext: outputs extension for the media file
    """
    allowed_ext = ['.mp4', ".mov", ".wmv", ".flv", ".avi", ".avchd", ".webm", ".mkv"]
    output_fn = f"{output_file}.{output_ext}"
    _, ext = os.path.splitext(os.path.join(file_path, media_file))

    if ext.lower() not in allowed_ext:

        ext = ", ".join(allowed_ext)
        print(f"Unknown format! try using from one of these formats{ext}")

    else:
        # do the processing
        clip = VideoFileClip(os.path.join(file_path, media_file))
        clip.audio.write_audiofile(os.path.join(file_path, output_fn))

    return output_fn



def process_transcription(url, file_path):

    """
    flask-executor for subprocessing
    """
    vid_id = url.split("=")[-1]
    transcription =  audio_to_text(url=url, file_path=file_path)
    summary = summarizer(transcription)
    keywords = keyword_extractor(transcription)
    classifications = predict_tags(transcription)[0]
    confidence_list = classifications['confidences']
    tags = [conf['label'] for conf in confidence_list] # if conf['confidence'] >= 0.3]
    tags_text = ", ".join(tags[:5])

    return vid_id, transcription, summary, keywords, tags_text


def audio_to_text_v2(url=None, audio_file=None, file_path=None):
    """
    Args:
        link: [str] -> takes a youtube video link
    returns: transcribed text from video 

    """
    print(f"{file_path}")
    print(url)
    # device = "cuda" if torch.cuda.is_available() else "cpu"
    # bs = 16

    API_TOKEN = "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"
    API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v2"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}


    if url:

        f_name = 'audio_file.mp4' # the file name to save with
        yt = YouTube(url)

        # if GPU available run this block
        # if device == 'cuda':
        # compute_type = "float16"
        # model = whisperx.load_model("large-v2", device, compute_type=compute_type)
        try:
            yt.streams.filter(only_audio=True)
            stream = yt.streams.get_by_itag(139)
            stream.download(file_path, f_name)
            # audio = whisperx.load_audio(os.path.join(file_path, f_name))
            # result = model.transcribe(audio, batch_size=bs, language='en')

            with open(f"{file_path}/{f_name}", "rb") as f:
                data = f.read()
                response = requests.post(API_URL, headers=headers, data=data)
                res = response.json()['text']
            # res = [ i['text'] for i in result['segments'] ]
            # os.remove(f"static/{f_name}")

            return res

        except AgeRestrictedError:
            res = ""
            return res

    # else:   # else run this block

    #     compute_type = "int8"
    #     model = whisperx.load_model("large-v2", device, compute_type=compute_type)

    #     try:
    #         yt.streams.filter(only_audio=True)
    #         stream = yt.streams.get_by_itag(139)
    #         print("dowload strat")
    #         stream.download(file_path, f_name)
    #         print(f"saved to {file_path}/{f_name}")
    #         print(f"{file_path}, {f_name}")
    #         audio = whisperx.load_audio(f"{file_path}/{f_name}")
    #         print("audio loaded")
    #         result = model.transcribe(audio, language='en')
    #         print("finishied transcribing")
    #         res = [ i['text'] for i in result['segments'] ]
    #         # os.remove(f"static/{f_name}")

    #         print("returnin results")

    #         return res[0]

    #     except AgeRestrictedError:

    #         res = ""
    #         return res

    elif audio_file:
        # so, It's already in the audio format
        # if device == 'cuda':
        #     compute_type = "float16"
        #     model = whisperx.load_model("large-v2", device, compute_type=compute_type)
        #     audio = whisperx.load_audio(os.path.join(file_path, audio_file)) # load the audio file
        #     result = model.transcribe(audio, batch_size=bs, language='en')
        #     res = [ i['text'] for i in result['segments'] ]
        #     # os.remove(os.path.join())
        #     return res[0]

        # compute_type = "int8"
        # model = whisperx.load_model("large-v2", device, compute_type=compute_type)
        # audio = whisperx.load_audio(os.path.join(file_path, audio_file)) # load the audio file
        # result = model.transcribe(audio, language='en')
        # res = [ i['text'] for i in result['segments'] ]

        with open(f"{file_path}/{audio_file}", "rb") as f:
            data = f.read()
            response = requests.post(API_URL, headers=headers, data=data)
            res = response.json()['text']

    return res
