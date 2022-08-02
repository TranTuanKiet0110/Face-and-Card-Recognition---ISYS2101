import cv2.cv2 as cv2
import numpy as np
import face_recognition
import os
import re

path = 'images file'
images = []
classNames = []
myList = os.listdir(path)
getName = []
print(myList)

for img in myList:
    currentImg = cv2.imread(f'{path}/{img}')
    images.append(currentImg)
    classNames.append(os.path.splitext(img)[0])
print(classNames)

for name in classNames:
    res = re.sub(' \d+', " ", name)
    getName.append(res)
print(getName)

def findEncoding(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

encodeListKnown = findEncoding(images)
print('Encoding Complete')

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgSmall = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgSmall = cv2.cvtColor(imgSmall, cv2.COLOR_BGR2RGB)

    faceCurrentFrame = face_recognition.face_locations(imgSmall)
    encodeCurrentFrame = face_recognition.face_encodings(imgSmall, faceCurrentFrame)

    for encodeFace, faceLoc in zip(encodeCurrentFrame, faceCurrentFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = getName[matchIndex].upper()
            print(name)

    cv2.imshow('Webcam', img)
    cv2.waitKey(10)