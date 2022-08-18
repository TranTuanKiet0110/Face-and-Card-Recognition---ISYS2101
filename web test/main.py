from flask import Flask, render_template, request, redirect
import os
import pytesseract
from PIL import Image
import re

app = Flask(__name__)

app.config['IMAGE_UPLOADS'] = 'C:\Face-and-Card-Recognition---ISYS2101\web test\static\image'
from werkzeug.utils import secure_filename

@app.route("/", methods=['POST', "GET"])
def upload_image():
    if request.method == "POST":

        image = request.files['file']

        pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'  # pytesseract location

        if image.filename == '':
            print("File name is invalid")
            return redirect(request.url)

        filename = "id.jpg"
        print(filename)
        path = f"static/image/{filename}"  # image path

        basedir = os.path.abspath(os.path.dirname(__file__))
        image.save(os.path.join(basedir, app.config["IMAGE_UPLOADS"], filename))

        img = Image.open(path)
        text = pytesseract.image_to_string(img)  # scan text on image

        """write into text file"""
        with open('save_log.txt', 'w') as file:
            file.writelines(f'{str(text)}')
        file.close()

        """remove blank rows in text file"""
        output = ""
        with open('save_log.txt') as file:
            for line in file:
                if not line.isspace():
                    output += line
        file.close()

        f = open('save_log.txt', 'w')
        f.write(output)
        f.close()

        """remove unwanted characters in text file"""
        s = open('save_log.txt').read()
        new_str = re.sub(r'[^a-zA-Z\s\d\n:]', '', s)
        f = open('save_log.txt', 'w')
        f.write(new_str)
        f.close()

        """remove blank space at the start of every lines in text file"""
        output2 = ""
        with open('save_log.txt') as file:
            for line in file:
                output2 += line.lstrip(' ')
        file.close()
        f = open('save_log.txt', 'w')
        f.write(output2)
        f.close()

        """function to record data into csv file"""

        def recordData(school, sName, sID, exDate):
            with open('cardData.csv', 'r+') as file:
                file.writelines(f"School, Student Name, Student ID, ex-Date")
                file.writelines(f'\n{school},{sName},{sID},{exDate}')

        """put data into dataList"""
        with open('save_log.txt', 'r') as file:
            dataList = []
            for line in file:
                strip_lines = line.strip()
                dataList.append(strip_lines)
            print(dataList)
            school = dataList[0] + ' ' + dataList[1]
            sName = dataList[2]
            sID = dataList[3]
            exDate = dataList[4]
            recordData(school, sName, sID, exDate)  # call function
        file.close()
        # return render_template("readText.html")
        return redirect('/userinfo')
    return render_template("index.html")

@app.route('/userinfo', methods=['GET', 'POST'])
def userinfo():
    with open('save_log.txt', 'r') as file:
        infoList = []
        for line in file:
            strip_lines = line.strip()
            infoList.append(strip_lines)
        print(infoList)
        school = infoList[0] + ' ' + infoList[1]
        sname = infoList[2]
        sid = infoList[3]
        exdate = infoList[4]
    file.close()

    return render_template("readText.html", school=school, sname=sname, sid=sid, exdate=exdate)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500, debug=True)