#importing libraries
import cv2
import numpy as np


#function to stack images

def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[2] == imgArray[0][0].shape[2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

#reading image
frog_img = cv2.imread('frog.jpg')

#define kernel
kernel = np.ones((5, 5), np.uint8)

#changing colors of image
frog_imgGray = cv2.cvtColor(frog_img, cv2.COLOR_BGR2GRAY)
frog_colour = cv2.cvtColor(frog_img, cv2.COLOR_BGR2HSV)

#imaking blury image
blurry_frog = cv2.GaussianBlur(frog_imgGray, (5,7), 0)
frogBlur = cv2.medianBlur(frog_imgGray, 7, 0)

#edge detector
frog_canny = cv2.Canny(frog_imgGray, 100,100)

#image dialation
frog_dialation = cv2.dilate(frog_canny, kernel, iterations=1)

#image erosion//making the lnes thinner
frog_erosion = cv2.erode(frog_dialation, kernel, iterations=1)


imgStack= stackImages(0.9,([frog_img,frog_imgGray,blurry_frog,frogBlur,frog_canny]))

#cv2.imshow("normal", frog_img)
#cv2.imshow("colour", frog_colour)
#cv2.imshow("Gray image", frog_imgGray)
#cv2.imshow("Gray Blury image", blurry_frog)
#cv2.imshow("More blur", frogBlur)
#cv2.imshow("Canny", frog_canny)
#cv2.imshow("Dilation", frog_dialation)
#cv2.imshow("Erosion", frog_erosion)

cv2.imshow("stacked images", imgStack)
cv2.waitKey(0)
