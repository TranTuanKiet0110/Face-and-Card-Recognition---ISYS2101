from flask import Flask, render_template, request, redirect, Response
import os
import pytesseract
from PIL import Image
import re
import cv2.cv2 as cv2
import numpy as np
import face_recognition
import datetime

app = Flask(__name__)

app.config['IMAGE_UPLOADS'] = 'C:\\Face-and-Card-Recognition---ISYS2101\\static\\image'

@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/newFaceScan", methods=['POST', "GET"])
def backfaceID():
    return render_template("faceID.html")

@app.route("/homepage", methods=['POST', "GET"])
def returnHomepage():
    return render_template("homepage.html")

@app.route('/openlogin', methods=['POST', "GET"])
def openLogin():
    return render_template("LogInLogOut.html")

@app.route('/adminAuth', methods=['POST', "GET"])
def adminAuth():
    username = request.form['username']
    password = request.form['password']
    if username == "admin" and password == "admin":
        filename = ""
        dateList = []
        for file in os.listdir("C:\Face-and-Card-Recognition---ISYS2101\log"):
            filename = file
            dateList.append(str(filename).replace(".txt", ''))
        latest = str(filename).replace(".txt", '')
        output = ""
        with open("log/" + str(filename), "r+") as file:
            for line in file:
                if not line.isspace():
                    output += line
        file.close()
        with open("log/" + str(filename), "w") as file:
            file.writelines(output)
        file.close()
        infos = open("log/" + str(filename)).readlines()
        list = []
        for info in infos:
            entry = tuple(x.strip() for x in info.split(','))
            list.append(entry)
        entry = tuple(list)
        return render_template("adminAuthentication.html", latest=latest, column_names=['Student number', 'Student name', 'Time'], entry=entry, dateList=dateList)
    return render_template("adminInvalid.html")

@app.route('/viewEntry', methods=['POST', "GET"])
def chooseDate():
    dateList = []
    selectedDate = request.form['date']
    filename = ""
    for file in os.listdir("C:\Face-and-Card-Recognition---ISYS2101\log"):
        filename = file
        dateList.append(str(filename).replace(".txt", ''))
    output = ""
    with open("log/" + str(selectedDate) + ".txt", "r+") as file:
        for line in file:
            if not line.isspace():
                output += line
    file.close()
    with open("log/" + str(selectedDate) + ".txt", "w") as file:
        file.writelines(output)
    file.close()
    infos = open("log/" + str(selectedDate) + ".txt").readlines()
    list = []
    for info in infos:
        entry = tuple(x.strip() for x in info.split(','))
        list.append(entry)
    entry = tuple(list)
    return render_template("adminAuthentication.html", column_names=['Student number', 'Student name', 'Time'],
                           entry=entry, latest=selectedDate, dateList=dateList)

@app.route('/successValidation', methods=['POST', "GET"])
def confirmLogin():
    with open("current_name.txt", 'r+') as file:
        infoDataList = []
        for line in file:
            strip_lines = line.strip()
            infoDataList.append(strip_lines)
        name = infoDataList[0].replace('ÿþ', '')
    file.close()
    required_data = os.path.join('user_data', name, 'user_info.txt')
    with open(required_data, 'r+') as file:
        infoDataList = []
        for line in file:
            strip_lines = line.strip()
            infoDataList.append(strip_lines)
        school = infoDataList[0]
        sname = infoDataList[1]
        sid = infoDataList[2]
        exdate = infoDataList[3]
    file.close()
    return render_template("successValidation.html", school=school, sname=sname, sid=sid, exdate=exdate)

@app.route('/faceScan')
def openScan():
    return render_template("faceID.html")

encodeListKnown = ""
def gen():
    """Create lists to store image"""
    path = "user_image"
    images = []
    classNames = []
    myList = os.listdir(path)  # read file in path
    getName = []  # get name of the image

    """Loop through myList"""
    for img in myList:
        currentImg = cv2.imread(f'{path}/{img}')  # read each image in the folder
        images.append(currentImg)  # append to the images list
        classNames.append(os.path.splitext(img)[0])  # split text to get the name of the image

    """Loop through classNames list"""
    for name in classNames:
        res = re.sub('..$', "", name)  # delete numeric characters in image name
        getName.append(res)  # append to getName list

    """function to encode all of the images in images list"""

    def findEncoding(images):
        encodeList = []  # create new list
        for img in images:  # loop through images list
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # convert to cvtColor file
            encode = face_recognition.face_encodings(img)[0]  # encode the cvtColor file
            encodeList.append(encode)  # store in encodeList
        return encodeList

    encodeListKnown = findEncoding(images)  # call the function
    print('Encoding Complete')


    cap = cv2.VideoCapture(0)
    known = []
    while True:
        ret, frame = cap.read()

        imgSmall = cv2.resize(frame, (0, 0), None, 0.25, 0.25)  # resize image capture by webcam
        imgSmall = cv2.cvtColor(imgSmall, cv2.COLOR_BGR2RGB)  # convert the resized image to cvtColor file

        faceCurrentFrame = face_recognition.face_locations(imgSmall)  # find the face location
        encodeCurrentFrame = face_recognition.face_encodings(imgSmall,
                                                             faceCurrentFrame)  # encode the current frame capture by webcam
        current_name = []
        for encodeFace, faceLoc in zip(encodeCurrentFrame, faceCurrentFrame):
            matches = face_recognition.compare_faces(encodeListKnown,
                                                     encodeFace)  # find matches image with the person in the webcam
            faceDis = face_recognition.face_distance(encodeListKnown,
                                                     encodeFace)  # find face distance; the small the faceDis is, the more it matched
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = getName[matchIndex].upper()  # get username which is the name of the image
                print(name)
                current_name.append(name)
                """draw rectangle around the face location on the webcam screen"""
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4  # the webcam image is resized above so we have to multiply by 4
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255),
                            2)  # write the user name below the rectangle

                if name not in known:
                    known.append(name)
                    user_info = os.path.join('user_data', name, 'user_info.txt')
                    with open(user_info, 'r') as file:
                        infoList = []
                        for line in file:
                            strip_lines = line.strip()
                            infoList.append(strip_lines)
                        sname = infoList[1]
                        sid = infoList[2]
                    file.close()
                    with open('current_name.txt', 'w') as file:
                        file.writelines(f"{str(current_name[0])}")
                    file.close()
                    today = datetime.date.today()
                    log = os.path.join('log', str(today) + '.txt')
                    with open(log, 'a+') as file:
                        now = datetime.datetime.now()
                        dtString = now.strftime('%H:%M:%S')
                        file.writelines(f"\n{str(sid)},{str(sname)},{str(dtString)}")
                    file.close()
        if not ret:
            print("Error: failed to capture image")
            break

        cv2.imwrite('capture.jpg', frame)
        cv2.waitKey(1)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('capture.jpg', 'rb').read() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/register", methods=['POST', "GET"])
def openRegister():
    return render_template("uploadID.html")

@app.route("/viewID", methods=['POST', "GET"])
def uploadID():
    if request.method == "POST":

        image = request.files['file']

        pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'  # pytesseract location
#         pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'
        if image.filename == '':
            return redirect(request.url)

        filename = "id.jpg"
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
            if len(infoList) == 0:
                school = "None"
                sname = "None"
                sid = "None"
                exdate = "None"
            elif len(infoList) == 1:
                school = "None"
                sname = "None"
                sid = "None"
                exdate = "None"
            elif len(infoList) == 2:
                school = infoList[0] + ' ' + infoList[1]
                sname = "None"
                sid = "None"
                exdate = "None"
            elif len(infoList) == 3:
                school = infoList[0] + ' ' + infoList[1]
                sname = infoList[2]
                sid = "None"
                exdate = "None"
            elif len(infoList) == 4:
                school = infoList[0] + ' ' + infoList[1]
                sname = infoList[2]
                sid = "s" + infoList[3]
                exdate = "None"
            else:
                school = infoList[0] + ' ' + infoList[1]
                sname = infoList[2]
                sid = "s" + infoList[3]
                exdate = infoList[4][13:29]
        file.close()
        return render_template("viewInfo.html", school=school, sname=sname, sid=sid, exdate=exdate)

@app.route("/edit", methods=['POST', "GET"])
def edit():
    with open('save_log.txt', 'r') as file:
        infoList = []
        for line in file:
            strip_lines = line.strip()
            infoList.append(strip_lines)
        school = infoList[0] + ' ' + infoList[1]
        sname = infoList[2]
        sid = "s" + infoList[3]
        exdate = infoList[4][13:29]
    file.close()
    return render_template("editInfo.html", school=school, sname=sname, sid=sid, exdate=exdate)

@app.route("/uploadImage", methods=['POST', 'GET'])
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
    return render_template('uploadYourImage.html')

@app.route("/uploadImg", methods=['POST', 'GET'])
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
    return render_template('uploadYourImage.html')

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
        school = infoList[0]
        sname = infoList[1]
        sid = infoList[2]
        exdate = infoList[3]
    file.close()
    return render_template("editInfoSecond.html", school=school, sname=sname, sid=sid, exdate=exdate)

@app.route("/viewEdit", methods=['POST'])
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

@app.route("/successfullyRegister", methods=['POST', "GET"])
def uploadImage():
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

    if request.method == "POST":

        image = request.files['file']

        if image.filename == '':
            return redirect(request.url)
        filename = sid + "_1.jpg"
        image.save(os.path.join('user_image', filename))
        folder_name = sid.upper()
        folder = os.path.join('user_data', folder_name)
        user_info = os.path.join('user_data', folder_name, 'user_info.txt')
        if school == "RMIT UNIVERSITY":
            os.makedirs(folder)
            with open(user_info, 'w') as file:
                file.writelines(f'{str(school)}\n{str(sname)}\n{str(sid)}\n{str(exdate)}')
        else:
            return render_template("invalidSchool.html")
        return render_template("verifySuccessful.html")

if __name__ == '__main__':
    app.run(host='localhost', port=5500, debug=True)
