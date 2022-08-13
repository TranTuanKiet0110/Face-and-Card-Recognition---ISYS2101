"""Import library"""
import cv2.cv2 as cv2
import numpy as np
import face_recognition
import os
import re
import datetime

"""Create lists to store image"""
path = 'images file'  # file path
images = []
classNames = []
myList = os.listdir(path)  # read file in path
getName = []  # get name of the image
print(myList)

"""Loop through myList"""
for img in myList:
    currentImg = cv2.imread(f'{path}/{img}')  # read each image in the folder
    images.append(currentImg)  # append to the images list
    classNames.append(os.path.splitext(img)[0])  # split text to get the name of the image
print(classNames)

"""Loop through classNames list"""
for name in classNames:
    res = re.sub(' \d+', " ", name)  # delete numeric characters in image name
    getName.append(res)  # append to getName list
print(getName)

"""function to encode all of the images in images list"""
def findEncoding(images):
    encodeList = []  # create new list
    for img in images:  # loop through images list
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # convert to cvtColor file
        encode = face_recognition.face_encodings(img)[0]  # encode the cvtColor file
        encodeList.append(encode)  # store in encodeList
    return encodeList


"""function to record attendance"""
def recordAttendance(name):
    with open('attendance.csv', 'r+') as file:
        myDataList = file.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.datetime.now()
            dtString = now.strftime('%H:%M:%S')
            file.writelines(f'\n{name},{dtString}')
    file.close()
encodeListKnown = findEncoding(images)  # call the function
print('Encoding Complete')

"""Implement webcam"""
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgSmall = cv2.resize(img, (0, 0), None, 0.25, 0.25)  # resize image capture by webcam
    imgSmall = cv2.cvtColor(imgSmall, cv2.COLOR_BGR2RGB)  # convert the resized image to cvtColor file

    faceCurrentFrame = face_recognition.face_locations(imgSmall)  # find the face location
    encodeCurrentFrame = face_recognition.face_encodings(imgSmall,
                                                         faceCurrentFrame)  # encode the current frame capture by webcam

    for encodeFace, faceLoc in zip(encodeCurrentFrame, faceCurrentFrame):
        matches = face_recognition.compare_faces(encodeListKnown,
                                                 encodeFace)  # find matches image with the person in the webcam
        faceDis = face_recognition.face_distance(encodeListKnown,
                                                 encodeFace)  # find face distance; the small the faceDis is, the more it matched
        print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = getName[matchIndex].upper()  # get username which is the name of the image
            print(name)
            """draw rectangle around the face location on the webcam screen"""
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4  # the webcam image is resized above so we have to multiply by 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255),
                        2)  # write the user name below the rectangle
            recordAttendance(name)  # call the attendance function

    cv2.imshow('Webcam', img)  # show webcam screen
    cv2.waitKey(1)