from transform import four_point_transform
#파이썬 파일
from skimage.filters import threshold_local
import numpy as np
import argparse
import imutils
import cv2
def image_parsing():
    # 아규먼트 파싱을 한다
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required = False,default=r"/home/powershin/image.jpg",
        help = "Path to the image to be scanned")
    args = vars(ap.parse_args())

    # 이미지를 로드하고 source 좌표들을 가져오자 ((x,y) 리스트).
    # 주 의: eval 함수를 사용하는 것은 별로 좋지 않지만
    #        이번 예제에는 그냥 쓰도록 하자.
    image = cv2.imread(args["image"])
    ratio = image.shape[0] / 500.0
    orig = image.copy()
    image = imutils.resize(image, height = 500)
    # convert the image to grayscale, blur it, and find edges
    # in the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 75, 200)
    # show the original image and the edge detected image
    # find the contours in the edged image, keeping only the
    # largest ones, and initialize the screen contour
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]
    # loop over the contours
    screenCnt=0
    for c in cnts:
        
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        # if our approximated contour has four points, then we
        # can assume that we have found our screen
        if len(approx) == 4:
            screenCnt = approx
            break
    # show the contour (outline) of the piece of paper
    
    if type(screenCnt)==int:
        return False
    cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)

    warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)
    # convert the warped image to grayscale, then threshold it
    # to give it that 'black and white' paper effect
    warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    T = threshold_local(warped, 11, offset = 10, method = "gaussian")
    warped = (warped > T).astype("uint8") * 255
    cv2.imwrite("image1.jpg",imutils.resize(warped, height = 650))
    return True