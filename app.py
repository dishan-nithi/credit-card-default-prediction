from flask import Flask, render_template, request, session, redirect, url_for
import os
import numpy as np
import pandas as pd
from default_predictor.pipeline.prediction import PredictionPipeline

app = Flask(__name__)
app.secret_key = "supersecretkey" 

UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        if 'attachment' not in request.files:
            return 'No file uploaded',400
        
        file = request.files['attachment']
        
        if file.name == '':
            return 'No file uploaded',400
        
        
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
        session['uploaded_file_path'] = file_path
        
        return 'Saved'
    
    return render_template("index.html")

@app.route('/train', methods=['GET'])
def training():
    os.system("python main.py")
    return "Training successful"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
