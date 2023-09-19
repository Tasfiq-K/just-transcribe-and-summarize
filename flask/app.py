import os
import requests
from functions import predict_tags, audio_to_text, summarizer, keyword_extractor, media_to_audio
from flask import Flask, render_template, request


app = Flask(__name__)

# UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static/')
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/", methods=['GET', 'POST']) # call the home function when submitting the form to the current route
def home():

    input_text = ""
    save_loc = "static"


    if request.method == 'POST':
        input_text = request.form.get('input_text', '')
        input_link = request.form.get('input_link', '')
        media_file = request.files['input_media']
        print(input_text)

        if input_link:
            transcription = audio_to_text(url=input_link, file_path=save_loc)
            summary = summarizer(transcription)
            keywords = keyword_extractor(transcription)
            classifications = predict_tags(transcription)[0]
            confidence_list = classifications['confidences']
            tags = [conf['label'] for conf in confidence_list if conf['confidence'] >= 0.3]
            tags_text = ""
            tags_text = ", ".join(tags)

            print(tags_text)
            return render_template("results.html", input_text=input_text, output_text=tags_text)

        if media_file:
            # check and save the media file
            if media_file.filename != "":
                fn = media_file.filename
                if not os.path.exists(save_loc):
                    os.mkdir('static')
                    media_file.save(os.path.join(save_loc, fn))
                else:
                    media_file.save(os.path.join(save_loc, fn))
                
                # convert media to text
                transcription = audio_to_text(audio_file=media_to_audio(fn, save_loc), file_path=save_loc)
                
                summary = summarizer(transcription) # get the summary
                keywords = keyword_extractor(transcription) # get the keywords
                
                # classification stuff
                classifications = predict_tags(transcription)[0]    
                confidence_list = classifications['confidences']
                tags = [conf['label'] for conf in confidence_list if conf['confidence'] >= 0.3]
                tags_text = ""
                tags_text = ", ".join(tags)
                
            return render_template("results.html", input_text=input_text, output_text=tags_text)

            
            # else:
        
        if input_text:
            transcription = input_text
            summary = summarizer(transcription)
            keywords = keyword_extractor(transcription)
            classifications = predict_tags(transcription)[0]
            confidence_list = classifications['confidences']
            tags = [ conf['label'] for conf in confidence_list if conf['confidence'] >= 0.3]
            tags_text = ""
            tags_text = ", ".join(tags)

        return render_template("resutls.html", input_text=input_text, output_text=tags_text)

    return render_template("home.html")



if __name__ == "__main__":
    app.run(debug=True)
