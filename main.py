import cv2
import numpy as np
import imutils
import easyocr
import os
from datetime import datetime


def display(name, images):
    cv2.imshow(name, images)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


img = cv2.imread('2.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
display('gray image', gray)

bfilter = cv2.bilateralFilter(gray, 11, 17, 17)  # Noise reduction
edged = cv2.Canny(bfilter, 30, 200)  # Edge detection


keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(keypoints)
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

location = None
for contour in contours:
    approx = cv2.approxPolyDP(contour, 10, True)
    if len(approx) == 4:
        location = approx
        x, y, w, h = cv2.boundingRect(location)
        break

mask = np.zeros(gray.shape, np.uint8)
new_image = cv2.drawContours(mask, [location], 0, 255, -1)
new_image = cv2.bitwise_and(img, img, mask=mask)


(x1, y1) = np.where(mask == 255)
(x2, y2) = (np.min(x1), np.min(y1))
(x3, y3) = (np.max(x1), np.max(y1))
license_plate = gray[x2:x3 + 1, y2:y3 + 1]
display('License Plate', license_plate)


reader = easyocr.Reader(['bn'])
result = reader.readtext(license_plate, detail=0)
print(result)


city_name = result[0][0]
if city_name == 'ঢ':
  city_text = 'Dhaka'
elif city_name == 'চ':
  city_text = 'Chatto'

metro = 'Metro'

class_name = result[0][12]

if class_name == 'ক':
  class_text = 'Ka'
elif class_name == 'খ':
  class_text = 'Kha'
elif class_name == 'গ':
  class_text = 'Ga'
elif class_name == 'ঘ':
  class_text = 'Gha'
elif class_name == 'চ':
  class_text = 'Ca'
elif class_name == 'ছ':
  class_text = 'Cha'
elif class_name == 'থ':
  class_text = 'tha'
elif class_name == 'ট':
  class_text = 'Ta'
elif class_name == 'ঠ':
  class_text = 'Tha'
elif class_name == 'হ':
  class_text = 'Ha'
elif class_name == 'ন':
  class_text = 'Na'
elif class_name == 'ম':
  class_text = 'Mo'


N = ([int(n) for n in result[1] if n.isdigit()])
number = ''.join(map(str, N))
license_plate_name = number
number = number[:2] + '-' + number[2:]


txtToCsv = city_text +' '+ metro +'-'+ class_text + ' ' + number
text = city_text +' '+ metro +'-'+ class_text
text_num = number

#save license plate image#
arr = os.listdir('License Plate image')
i = len(arr)+1
cv2.imwrite('License Plate image/License {} No.{}.jpg'.format(int(license_plate_name),i), license_plate, [cv2.IMWRITE_JPEG_QUALITY, 100])

#save text, Date and time into csv file#
now = datetime.now()
now = now.strftime("Date : %B %d %Y, Time : %I:%M:%S %p")
print(now)

LicenseText = open('CSV File/license_plate.csv','a+')
LicenseText.write((txtToCsv + ', ' + now))
LicenseText.write("\n")
LicenseText.close()
print("Text Saved Successfully into CSV File")


#show the final result#
img = cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 3)
img = cv2.putText(img, text.upper(), (x + 15, y-30), cv2.FONT_HERSHEY_PLAIN, 1, (100, 0, 255), 0, cv2.LINE_AA)
img = cv2.putText(img, text_num.upper(), (x + 50, y-10), cv2.FONT_HERSHEY_PLAIN, 1, (100, 0, 255), 0, cv2.LINE_AA)
print("License plate : ", text.upper(), text_num)

display('main image', img)