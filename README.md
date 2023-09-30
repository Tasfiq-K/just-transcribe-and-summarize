# A Multilabel Text classifier with integrated transcriber and summarizer

<h1 align='center' style=color:#fe5e21;><strong>Just Transcribe and Summaraize</strong></h1>

A multipurpose text classification model transcribes speech from video/audio sources, summarizes, classifies and extracts important topics from the text. <br/>

If you Want to find out the transcriptions and the summarized version of your favorite video or text? May it be a lecture a vlog or a personal one with conversations in it or a long text/paragraph. This is the place then. You can have your video transcribed, summarized. Not only that, you will also be able to know the type of the video or text and important topics in it.

This model can classify **316** different types of tags of the text <br/>The keys of `json_files/tag_types_encoded.json` shows the different tags.
<br/>

# Data Collection

For training the data were collected from two sources. <br/>
* A kaggle dataset
* From Youtube through scraping.

Data from these sources were merged to create the final dataset which was used for training purpose. Checkout the `csv_files` for the scraped dataset from Youtube. Also, checkout the `csv_files/link.md` to find out about the the dataset from kaggle and the final **merged dataset**.

Data from Youtube were collected through web scraping. `Selenium 4.9.0` was used to do the scraping. Script for the scraping can be found in `scrapers` directory.

# Data Preparation

The data preparation part was very cruical for this project. The dataset from kaggle contains 190K+ data. So scaling down the data was necessary. I took 35% of the whole data and merged with the data scraped from youtube. So, the total size of the dataset became **68275**. 

Data scraped from youtube only contained the links of the video and the corresponding tags. To transcribe the text from the video [WhisperX](https://github.com/m-bain/whisperX) was used. The transcribing part took a lot of time. `notebook/video_transcribing.ipynb` file contains the whole process of video transcribing. `notebook/speech_text_preprocessing` contains the merging of the two datasets. 

# Model Training

For training the model `distilroberta-base` from HuggingFace along with `blurr` and `fastai` was used. The traininig part consists two phases. First, training with freezed layers, then with unfreezed layers. Achieved 99% accuracy after training for 5 epochs. Model training notebook can be found the `notebook` directory.

## Techincal Details

The training was done in Google Colaboratory environment on a T4 GPU with 15 GB VRAM. At training on freezed layers a learning rate of `3.8e-3` was used which was determined by using fastai's `lr_find` function. The training consists of 2 epochs. Later at unfreezed state more 3 epoch were trained using learning rates between `1.5e-04 to 2.5e-6`. 

# Model Compression & ONNX Inference

The trained model has a memory of 317MB. Compressed this model using ONNX quantization and brought it under 80MB.

**F1 Scores**

`F1 Score (Micro) = 42.6` <br/>

`F1 Score (Macro) = 32.3`

# Demos

# Limitations

# Contributions


