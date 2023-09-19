import requests
from flask import Flask, render_template, request
from functions import predict_tags

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST']) # call the home function when submitting the form to the current route
def home():
    
    input_text = ""
    

    if request.method == 'POST':
        input_text = request.form.get('input_text', '')
        input_link = request.form.get('input_link', '')
        media_file = request.files['input_media']
        print(input_text)

        classifications = predict_tags(input_text)[0]
        confidence_list = classifications['confidences']
        tags = [conf['label'] for conf in confidence_list if conf['confidence'] >= 0.3]
        tags_text = ""

        # for idx, task in enumerate(tasks):
        #     task_text = task_text + task
        #     if idx != len(tasks)-1:
        #         task_text = task_text + ", "

        tag_text = ", ".join(tags)

        print(tag_text)
        return render_template("results.html", input_text=input_text, output_text=tag_text)
    else:
        return render_template("results.html")



if __name__ == "__main__":
    app.run(debug=True)