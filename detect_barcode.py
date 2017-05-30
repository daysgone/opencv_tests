# import the necessary packages
import numpy as np

import cv2

print cv2.__version__
def detect(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # compute the Scharr gradient magnitude representation of the images
    # in both the x and y direction
    gradX = cv2.Sobel(gray, ddepth = cv2.CV_32F, dx = 1, dy = 0, ksize = -1)

    gradY = cv2.Sobel(gray, ddepth = cv2.CV_32F, dx = 0, dy = 1, ksize = -1)

    # subtract the y-gradient from the x-gradient
    gradient = cv2.subtract(gradX, gradY)
    gradient = cv2.convertScaleAbs(gradient)

    # blur and threshold the image
    #blurred = cv2.blur(gradient, (9, 9))
    #(_, thresh) = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)

    # test
    blur = cv2.GaussianBlur(gradient, (5, 5), 0)
    ret3, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    cv2.imshow("thresh", thresh)
    cv2.imshow("blur", blur)
    # construct a closing kernel and apply it to the thresholded image
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # perform a series of erosions and dilations
    closed = cv2.erode(closed, None, iterations = 4)
    closed = cv2.dilate(closed, None, iterations = 4)

    # find the contours in the thresholded image, then sort the contours
    # by their area, keeping only the largest one
    (_, cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #cv2.imshow("image", closed)
    if len(cnts) is not 0:
        c = sorted(cnts, key = cv2.contourArea, reverse = True)[0]

        # compute the rotated bounding box of the largest contour
        rect = cv2.minAreaRect(c)
        #box = np.int0(cv2.cv.BoxPoints(rect))
        box = np.int0(cv2.boxPoints(rect))
        return box

    return False

