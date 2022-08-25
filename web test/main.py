from flask import Flask, render_template, request, redirect
import os
import pytesseract
from PIL import Image
import re
from werkzeug.utils import secure_filename
app = Flask(__name__)

app.config['IMAGE_UPLOADS'] = 'C:\Face-and-Card-Recognition---ISYS2101\web test\static\image'

@app.route("/", methods=['POST', "GET"])
def uploadID():
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

        with open('save_log.txt', 'r') as file:
            infoList = []
            for line in file:
                strip_lines = line.strip()
                infoList.append(strip_lines)
            print(infoList)
            school = infoList[0] + ' ' + infoList[1]
            sname = infoList[2]
            sid = "s" + infoList[3]
            exdate = infoList[4][13:29]
        file.close()
        return render_template("viewInfo.html", school=school, sname=sname, sid=sid, exdate=exdate)
    return render_template("uploadID.html")

@app.route("/edit", methods=['POST', "GET"])
def edit():
    with open('save_log.txt', 'r') as file:
        infoList = []
        for line in file:
            strip_lines = line.strip()
            infoList.append(strip_lines)
        print(infoList)
        school = infoList[0] + ' ' + infoList[1]
        sname = infoList[2]
        sid = "s" + infoList[3]
        exdate = infoList[4][13:29]
    file.close()
    return render_template("editInfo.html", school=school, sname=sname, sid=sid, exdate=exdate)

@app.route("/confirm", methods=['POST', 'GET'])
def confirm():
    with open('save_log.txt', 'r') as file:
        infoConfirmList = []
        for line in file:
            strip_lines = line.strip()
            infoConfirmList.append(strip_lines)
        school = infoConfirmList[0] + ' ' + infoConfirmList[1]
        sname = infoConfirmList[2]
        sid = "s" + infoConfirmList[3]
        exdate = infoConfirmList[4][13:29]
    file.close()

    with open('save_log.txt', 'w') as f:
        f.writelines(f'{str(school)}\n{str(sname)}\n{str(sid)}\n{str(exdate)}')
    f.close()
    num = 5
    return render_template('uploadYourImage.html', number=num)

@app.route("/confirm1", methods=['POST', 'GET'])
def confirm1():
    with open('save_log.txt', 'r') as file:
        infoDataList = []
        for line in file:
            strip_lines = line.strip()
            infoDataList.append(strip_lines)
        school = infoDataList[0]
        sname = infoDataList[1]
        sid = infoDataList[2]
        exdate = infoDataList[3]
    file.close()
    with open('save_log.txt', 'w') as file:
        file.writelines(f'{str(school)}\n{str(sname)}\n{str(sid)}\n{str(exdate)}')
    file.close()
    num = 5
    return render_template('uploadYourImage.html', number=num)

@app.route("/editForm", methods=['POST'])
def editForm():
    with open('save_log.txt', 'r') as file:
        oldInfoList = []
        for line in file:
            strip_lines = line.strip()
            oldInfoList.append(strip_lines)
        old_school = oldInfoList[0] + ' ' + oldInfoList[1]
        old_sname = oldInfoList[2]
        old_sid = "s" + oldInfoList[3]
        old_exdate = oldInfoList[4][13:29]
    file.close()

    new_school = request.form['school']
    new_sname = request.form['sname']
    new_sid = request.form['sid']
    new_exdate = request.form['exdate']

    with open('save_log.txt', 'w') as file:
        if new_school == "" and new_sname == "" and new_sid == "" and new_exdate == "":
            file.writelines(f'{str(old_school)}\n{str(old_sname)}\n{str(old_sid)}\n{str(old_exdate)}')
        elif new_school == "" and new_sname == "" and new_sid == "":
            file.writelines(f'{str(old_school)}\n{str(old_sname)}\n{str(old_sid)}\n{str(new_exdate)}')
        elif new_school == "" and new_sname == "" and new_exdate == "":
            file.writelines(f'{str(old_school)}\n{str(old_sname)}\n{str(new_sid)}\n{str(old_exdate)}')
        elif new_school == "" and new_sid == "" and new_exdate == "":
            file.writelines(f'{str(old_school)}\n{str(new_sname)}\n{str(old_sid)}\n{str(old_exdate)}')
        elif new_sname == "" and new_sid == "" and new_exdate == "":
            file.writelines(f'{str(new_school)}\n{str(old_sname)}\n{str(old_sid)}\n{str(old_exdate)}')
        elif new_school == "" and new_sname == "":
            file.writelines(f'{str(old_school)}\n{str(old_sname)}\n{str(new_sid)}\n{str(new_exdate)}')
        elif new_school == "" and new_sid == "":
            file.writelines(f'{str(old_school)}\n{str(new_sname)}\n{str(old_sid)}\n{str(new_exdate)}')
        elif new_school == "" and new_exdate == "":
            file.writelines(f'{str(old_school)}\n{str(new_sname)}\n{str(new_sid)}\n{str(old_exdate)}')
        elif new_sname == "" and new_sid == "":
            file.writelines(f'{str(new_school)}\n{str(old_sname)}\n{str(old_sid)}\n{str(new_exdate)}')
        elif new_sname == "" and new_exdate == "":
            file.writelines(f'{str(new_school)}\n{str(old_sname)}\n{str(new_sid)}\n{str(old_exdate)}')
        elif new_sid == "" and new_exdate == "":
            file.writelines(f'{str(new_school)}\n{str(new_sname)}\n{str(old_sid)}\n{str(old_exdate)}')
        elif new_school == "":
            file.writelines(f'{str(old_school)}\n{str(new_sname)}\n{str(new_sid)}\n{str(new_exdate)}')
        elif new_sname == "":
            file.writelines(f'{str(new_school)}\n{str(old_sname)}\n{str(new_sid)}\n{str(new_exdate)}')
        elif new_sid == "":
            file.writelines(f'{str(new_school)}\n{str(new_sname)}\n{str(old_sid)}\n{str(new_exdate)}')
        elif new_exdate == "":
            file.writelines(f'{str(new_school)}\n{str(new_sname)}\n{str(new_sid)}\n{str(old_exdate)}')
        else:
            file.writelines(f'{str(new_school)}\n{str(new_sname)}\n{str(new_sid)}\n{str(new_exdate)}')
    file.close()

    with open('save_log.txt', 'r') as file:
        infoDataList = []
        for line in file:
            strip_lines = line.strip()
            infoDataList.append(strip_lines)
        school = infoDataList[0]
        sname = infoDataList[1]
        sid = infoDataList[2]
        exdate = infoDataList[3]
    file.close()
    return render_template("viewInfoSecond.html", school=school, sname=sname, sid=sid, exdate=exdate)

@app.route("/editSecond", methods=['POST', "GET"])
def editSecond():
    with open('save_log.txt', 'r') as file:
        infoList = []
        for line in file:
            strip_lines = line.strip()
            infoList.append(strip_lines)
        print(infoList)
        school = infoList[0]
        sname = infoList[1]
        sid = infoList[2]
        exdate = infoList[3]
    file.close()
    return render_template("editInfoSecond.html", school=school, sname=sname, sid=sid, exdate=exdate)

@app.route("/editFormSecond", methods=['POST'])
def editFormSecond():
    with open('save_log.txt', 'r') as file:
        oldInfoList = []
        for line in file:
            strip_lines = line.strip()
            oldInfoList.append(strip_lines)
        old_school = oldInfoList[0]
        old_sname = oldInfoList[1]
        old_sid = oldInfoList[2]
        old_exdate = oldInfoList[3]
    file.close()

    new_school = request.form['school']
    new_sname = request.form['sname']
    new_sid = request.form['sid']
    new_exdate = request.form['exdate']

    with open('save_log.txt', 'w') as file:
        if new_school == "" and new_sname == "" and new_sid == "" and new_exdate == "":
            file.writelines(f'{str(old_school)}\n{str(old_sname)}\n{str(old_sid)}\n{str(old_exdate)}')
        elif new_school == "" and new_sname == "" and new_sid == "":
            file.writelines(f'{str(old_school)}\n{str(old_sname)}\n{str(old_sid)}\n{str(new_exdate)}')
        elif new_school == "" and new_sname == "" and new_exdate == "":
            file.writelines(f'{str(old_school)}\n{str(old_sname)}\n{str(new_sid)}\n{str(old_exdate)}')
        elif new_school == "" and new_sid == "" and new_exdate == "":
            file.writelines(f'{str(old_school)}\n{str(new_sname)}\n{str(old_sid)}\n{str(old_exdate)}')
        elif new_sname == "" and new_sid == "" and new_exdate == "":
            file.writelines(f'{str(new_school)}\n{str(old_sname)}\n{str(old_sid)}\n{str(old_exdate)}')
        elif new_school == "" and new_sname == "":
            file.writelines(f'{str(old_school)}\n{str(old_sname)}\n{str(new_sid)}\n{str(new_exdate)}')
        elif new_school == "" and new_sid == "":
            file.writelines(f'{str(old_school)}\n{str(new_sname)}\n{str(old_sid)}\n{str(new_exdate)}')
        elif new_school == "" and new_exdate == "":
            file.writelines(f'{str(old_school)}\n{str(new_sname)}\n{str(new_sid)}\n{str(old_exdate)}')
        elif new_sname == "" and new_sid == "":
            file.writelines(f'{str(new_school)}\n{str(old_sname)}\n{str(old_sid)}\n{str(new_exdate)}')
        elif new_sname == "" and new_exdate == "":
            file.writelines(f'{str(new_school)}\n{str(old_sname)}\n{str(new_sid)}\n{str(old_exdate)}')
        elif new_sid == "" and new_exdate == "":
            file.writelines(f'{str(new_school)}\n{str(new_sname)}\n{str(old_sid)}\n{str(old_exdate)}')
        elif new_school == "":
            file.writelines(f'{str(old_school)}\n{str(new_sname)}\n{str(new_sid)}\n{str(new_exdate)}')
        elif new_sname == "":
            file.writelines(f'{str(new_school)}\n{str(old_sname)}\n{str(new_sid)}\n{str(new_exdate)}')
        elif new_sid == "":
            file.writelines(f'{str(new_school)}\n{str(new_sname)}\n{str(old_sid)}\n{str(new_exdate)}')
        elif new_exdate == "":
            file.writelines(f'{str(new_school)}\n{str(new_sname)}\n{str(new_sid)}\n{str(old_exdate)}')
        else:
            file.writelines(f'{str(new_school)}\n{str(new_sname)}\n{str(new_sid)}\n{str(new_exdate)}')
    file.close()

    with open('save_log.txt', 'r') as file:
        newInfoList = []
        for line in file:
            strip_lines = line.strip()
            newInfoList.append(strip_lines)
        school = newInfoList[0]
        sname = newInfoList[1]
        sid = newInfoList[2]
        exdate = newInfoList[3]
    file.close()
    return render_template("viewInfoSecond.html", school=school, sname=sname, sid=sid, exdate=exdate)

@app.route("/uploadImage", methods=['POST', "GET"])
def uploadImage():
    with open('save_log.txt', 'r') as file:
        newInfoList = []
        for line in file:
            strip_lines = line.strip()
            newInfoList.append(strip_lines)
        sid = newInfoList[2]
    file.close()

    if request.method == "POST":

        image = request.files['file']

        if image.filename == '':
            print("File name is invalid")
            return redirect(request.url)
        filename = secure_filename(image.filename)
        folder_name = sid
        folder = os.path.join('user_image', folder_name)
        os.makedirs(folder)
        image.save(os.path.join(folder, filename))
        return render_template("uploadYourImage2.html", number=4)

@app.route("/uploadImage2", methods=['POST', "GET"])
def uploadImage2():
    with open('save_log.txt', 'r') as file:
        newInfoList = []
        for line in file:
            strip_lines = line.strip()
            newInfoList.append(strip_lines)
        sid = newInfoList[2]
    file.close()

    if request.method == "POST":

        image = request.files['file']

        if image.filename == '':
            print("File name is invalid")
            return redirect(request.url)
        filename = secure_filename(image.filename)
        folder_name = sid
        folder = os.path.join('user_image', folder_name)
        image.save(os.path.join(folder, filename))
        return render_template("uploadYourImage3.html", number=3)

@app.route("/uploadImage3", methods=['POST', "GET"])
def uploadImage3():
    with open('save_log.txt', 'r') as file:
        newInfoList = []
        for line in file:
            strip_lines = line.strip()
            newInfoList.append(strip_lines)
        sid = newInfoList[2]
    file.close()

    if request.method == "POST":

        image = request.files['file']

        if image.filename == '':
            print("File name is invalid")
            return redirect(request.url)
        filename = secure_filename(image.filename)
        folder_name = sid
        folder = os.path.join('user_image', folder_name)
        image.save(os.path.join(folder, filename))
        return render_template("uploadYourImage4.html", number=2)

@app.route("/uploadImage4", methods=['POST', "GET"])
def uploadImage4():
    with open('save_log.txt', 'r') as file:
        newInfoList = []
        for line in file:
            strip_lines = line.strip()
            newInfoList.append(strip_lines)
        sid = newInfoList[2]
    file.close()

    if request.method == "POST":

        image = request.files['file']

        if image.filename == '':
            print("File name is invalid")
            return redirect(request.url)
        filename = secure_filename(image.filename)
        folder_name = sid
        folder = os.path.join('user_image', folder_name)
        image.save(os.path.join(folder, filename))
        return render_template("uploadYourImage5.html", number=1)

@app.route("/uploadImage5", methods=['POST', "GET"])
def uploadImage5():
    with open('save_log.txt', 'r') as file:
        newInfoList = []
        for line in file:
            strip_lines = line.strip()
            newInfoList.append(strip_lines)
        sid = newInfoList[2]
    file.close()

    if request.method == "POST":

        image = request.files['file']

        if image.filename == '':
            print("File name is invalid")
            return redirect(request.url)
        filename = secure_filename(image.filename)
        folder_name = sid
        folder = os.path.join('user_image', folder_name)
        image.save(os.path.join(folder, filename))
        return render_template("uploadID.html")

if __name__ == '__main__':
    app.run(host='localhost', port=5500, debug=True)
