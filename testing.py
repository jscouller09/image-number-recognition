

import cv2
from PIL import Image
from pytesseract import pytesseract

# point to tesseract EXE
path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.tesseract_cmd = path_to_tesseract

# load colour image
img_col = cv2.imread('meter_read.jpg')

# convert image to grayscale
img_gry = cv2.cvtColor(img_col, cv2.COLOR_BGR2GRAY)
ret, thresh1 = cv2.threshold(img_gry, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
cv2.imwrite('threshold_image.jpg',thresh1)

rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
dilation = cv2.dilate(thresh1, rect_kernel, iterations = 5)
cv2.imwrite('dilation_image.jpg', dilation)

contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
im2 = img_col.copy()

for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
     
    # Draw the bounding box on the text area
    rect=cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
     
    # Crop the bounding box area
    cropped = im2[y:y + h, x:x + w]
    
    cv2.imwrite('rectanglebox.jpg',rect)
     
    # Using tesseract on the cropped image area to get text
    text = pytesseract.image_to_string(cropped)
    print(text)