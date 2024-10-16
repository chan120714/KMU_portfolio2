from gtts import gTTS
import pygame
import pytesseract
from PIL import Image
import cv2
from time import sleep
from pic import image_parsing

class ImageToText:
    def __init__(self, tesseract_cmd=None):
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    def convert(self, image_path, lang='eng'):
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image, lang=lang)
            return text
        except Exception as e:
            return str(e)

def threshold():
    image=cv2.imread('image.jpg')
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    height,width=gray.shape
    th=150
    
    ret,result=cv2.threshold(gray,th,255,cv2.THRESH_BINARY)
    cv2.imwrite("image2.jpg",result)
    return
while 1:
    cap=cv2.VideoCapture(0)

    res,frame=cap.read()
    if res:
        cv2.imwrite("image.jpg",frame)
        print('complete')
    else:
        print('error')
    cap.release()
    threshold()
    if image_parsing()==True:
        image_path = "image1.jpg"
    else:
        image_path = "image2.jpg"
    image_to_text = ImageToText()
    result = image_to_text.convert(image_path, lang='eng')
    pygame.init()
    if not result and image_parsing():
        result = image_to_text.convert("image2.jpg",lang='eng')
    if not result:
        result = image_to_text.convert("image.jpg",lang='eng')
    if not result:
        continue
    tts = gTTS(text=result, lang='en')
    tts.save("helloEN.mp3")
    print(result)
    sleep(1)
    pygame.mixer.music.load("helloEN.mp3")
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        sleep(0.1)