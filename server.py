from flask import Flask, render_template, request, jsonify
from train import make_prediction
from PIL import Image, ImageChops, ImageOps

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recognize', methods=['POST'])
def recognize():
    (digit, confidence) = make_prediction(request.files["img"])
    return jsonify({
        'digit': digit,
        'confidence': confidence
    })

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)