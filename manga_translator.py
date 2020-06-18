'''
Program manual
1. Drag your mouse on area you want. The ROI start from point that you left_button down until it up
2. Press s key to operate tesseract ocr if you draw a ROI properly, the program will send text via shell
   if not please try again (*** Don't press s more than 1 time without selecting ROI )
'''
import pytesseract 
from googletrans import Translator
from PIL import Image
import cv2
import os

cropping = False
rect = []

text = []
translated_text_eng = []
translated_text_th = []
text_position = []


def crop_image (event,x,y,flags,param):

    global rect , cropping

    if event == cv2.EVENT_LBUTTONDOWN:
        rect = [(x,y)]
        cropping = True

    elif event == cv2.EVENT_LBUTTONUP:
        rect.append((x,y))
        cropping = False

        cv2.rectangle(image,rect[0],rect[1] , (0,255,0) , 0)
    

translator = Translator()


image = cv2.imread('test.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.threshold(gray, 0, 255,
		cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
gray = cv2.medianBlur(gray, 1)

clone = gray.copy()
cv2.namedWindow('image')
cv2.setMouseCallback('image',crop_image)

while True :
        cv2.imshow('image',image)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('s'):  
            if len(rect) == 2:
                roi = clone[rect[0][1]:rect[1][1],rect[0][0]:rect[1][0]]
                filename = 'temp.png'
                cv2.imwrite(filename, roi)

                img = Image.open(filename)
                img = img.convert('L')

                text = pytesseract.image_to_string(img,lang ='jpn_vert')
                os.remove(filename)

                if len(text) != 0 :
                   translated_text_eng = translator.translate(text,src='ja',dest='en')
                   translated_text_th = translator.translate(text,src='ja',dest='th')
                   text_postion = (rect[0][0]-70,int((rect[0][1]+rect[1][1])*0.5))
                   cv2.putText(image, translated_text_eng.text ,text_postion ,
                               cv2.FONT_HERSHEY_SIMPLEX , 0.4, (255,0,0),0, cv2.LINE_AA)
                   print(text,'===>' ,translated_text_th.text )

                   rect = []
 
        
        elif key == ord('q'): 
            break
            

cv2.waitKey(0)
cv2.destroyAllWindows()
  

