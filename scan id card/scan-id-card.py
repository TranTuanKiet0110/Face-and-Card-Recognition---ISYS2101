import cv2
import pytesseract
from PIL import Image
import sys
import re

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
path = "id.jpg"
img = Image.open(path)
text = pytesseract.image_to_string(img)
with open('save_log.txt', 'w') as file:
    file.writelines(f'{str(text)}')
file.close()

output = ""
with open('save_log.txt') as file:
    for line in file:
        if not line.isspace():
            output += line
file.close()

f = open('save_log.txt', 'w')
f.write(output)
f.close()

s = open('save_log.txt').read()
new_str = re.sub(r'[^a-zA-Z\s\d\n:]', '', s)
f = open('save_log.txt', 'w')
f.write(new_str)
f.close()

output2 = ""
with open('save_log.txt') as file:
    for line in file:
        output2 += line.lstrip(' ')
file.close()
f = open('save_log.txt', 'w')
f.write(output2)
f.close()

with open('save_log.txt', 'r') as file:
    dataList = []
    for line in file:
        strip_lines = line.strip()
        dataList.append(strip_lines)
    print(dataList)
file.close()











