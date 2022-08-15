from flask import Flask, render_template, request, redirect
import os
import cv2
import pytesseract
from PIL import Image
import sys
import re
import csv
app = Flask(__name__)

app.config['IMAGE_UPLOADS'] = 'C:\Face-and-Card-Recognition---ISYS2101\web test\static\image'
from werkzeug.utils import secure_filename

@app.route("/home", methods=['POST', "GET"])
def upload_image():
    if request.method == "POST":

        image = request.files['file']

        if image.filename == '':
            print("File name is invalid")
            return redirect(request.url)

        filename = secure_filename(image.filename)

        basedir = os.path.abspath(os.path.dirname(__file__))
        image.save(os.path.join(basedir, app.config["IMAGE_UPLOADS"], filename))

        return render_template("index.html", filename=filename)


    return render_template("index.html")

@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='/images/'+filename), code=301)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500, debug=True)