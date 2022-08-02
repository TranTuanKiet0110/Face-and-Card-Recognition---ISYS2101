import cv2.cv2 as cv2
import numpy as np
import face_recognition

imgMusk = face_recognition.load_image_file('images file/elon musk.jpg')
imgMusk = cv2.cvtColor(imgMusk, cv2.COLOR_BGR2RGB)
imgTest = face_recognition.load_image_file('images file/elon musk test.jpg')
imgTest = cv2.cvtColor(imgTest, cv2.COLOR_BGR2RGB)

faceLoc = face_recognition.face_locations(imgMusk)[0]
encodeMusk = face_recognition.face_encodings(imgMusk)[0]
cv2.rectangle(imgMusk, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (255, 0, 255), 2)

faceLocTest = face_recognition.face_locations(imgTest)[0]
encodeTest = face_recognition.face_encodings(imgTest)[0]
cv2.rectangle(imgTest, (faceLocTest[3], faceLocTest[0]), (faceLocTest[1], faceLocTest[2]), (255, 0, 255), 2)

results = face_recognition.compare_faces([encodeMusk], encodeTest)
faceDis = face_recognition.face_distance([encodeMusk], encodeTest)
print(results, faceDis)
cv2.putText(imgTest, f'{results} {round(faceDis[0], 2)}', (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

cv2.imshow('Elon Musk', imgMusk)
cv2.imshow('Elon Musk Test', imgTest)
cv2.waitKey(0)
