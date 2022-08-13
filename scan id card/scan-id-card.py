"""import library"""
import cv2
import pytesseract
from PIL import Image
import sys
import re
import csv

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe' #pytesseract location
path = "id.jpg" #image path
img = Image.open(path)
text = pytesseract.image_to_string(img) #scan text on image

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
    recordData(school, sName, sID, exDate)
file.close()










