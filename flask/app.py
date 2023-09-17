import requests
from flask import Flask, render_template, request


app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    input_text = ""
    

    if request.method == 'POST':
        input_text = request.form.get('input_text', '')
        print(input_text)    
        output = predict_tasks(input_text)[0]
        confidence_list = output['confidences']
        tasks = [conf['label'] for conf in confidence_list if conf['confidence'] >= 0.3]
        task_text = ""

        # for idx, task in enumerate(tasks):
        #     task_text = task_text + task
        #     if idx != len(tasks)-1:
        #         task_text = task_text + ", "

        task_text = ", ".join(tasks)

        print(task_text)
        return render_template("home.html", input_text=input_text, output_text=task_text)
    else:
        return render_template("home.html")

def predict_tasks(input_text):
    response = requests.post("https://g0blas-paper-task-suggestion.hf.space/run/predict",
                             json={
                                 "data": [
                                     input_text
                                ]
                             }).json()
    data = response["data"]
    
    return data

if __name__ == "__main__":
    app.run(debug=True)