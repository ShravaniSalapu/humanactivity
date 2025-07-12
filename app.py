from flask import Flask, render_template, request, send_file
from ultralytics import YOLO
from PIL import Image, ImageDraw, ImageFont
import io
import os

app = Flask(__name__)
model = YOLO("C:/Users/ADMIN/Desktop/human/best.pt")  # Adjusted for local path
CLASS_NAMES = model.names
font = ImageFont.load_default()

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        if 'image' not in request.files:
            return "No image uploaded", 400
        file = request.files['image']
        image = Image.open(file.stream).convert("RGB")
        results = model(image)
        boxes = results[0].boxes.xyxy.cpu().numpy()
        scores = results[0].boxes.conf.cpu().numpy()
        labels = results[0].boxes.cls.cpu().numpy().astype(int)
        draw = ImageDraw.Draw(image)
        for box, label, score in zip(boxes, labels, scores):
            x1, y1, x2, y2 = box
            draw.rectangle([x1, y1, x2, y2], outline="blue", width=2)
            text = f"{CLASS_NAMES[label]}: {score:.2f}"
            draw.text((x1, y1 - 10), text, font=font, fill="green")
        img_io = io.BytesIO()
        image.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')
    return render_template("predict.html")

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)
