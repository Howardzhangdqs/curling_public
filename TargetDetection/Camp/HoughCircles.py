
from __future__ import division
import cv2
import numpy as np


def nothing(*arg):
    pass

# cv2.HoughCircles(coins_img_gray,
#                                     cv2.HOUGH_GRADIENT,
#                                     2,
#                                     100,
#                                     param1=100,
#                                     param2=250,
#                                     minRadius=100,
#                                     maxRadius=200)


icol = (2, 100, 100, 66, 0, 0)

cv2.namedWindow('colorTest')
# Lower range colour sliders.
cv2.createTrackbar('dp', 'colorTest', icol[0], 10, nothing)
cv2.createTrackbar('minDist', 'colorTest', icol[1], 1000, nothing)
cv2.createTrackbar('param1', 'colorTest', icol[2], 1000, nothing)
cv2.createTrackbar('param2', 'colorTest', icol[3], 1000, nothing)
cv2.createTrackbar('minRadius', 'colorTest', icol[4], 1000, nothing)
cv2.createTrackbar('maxRadius', 'colorTest', icol[5], 1000, nothing)

# Raspberry pi file path example.
# frame = cv2.imread('/home/pi/python3/opencv/color-test/colour-circles-test.jpg')
# Windows file path example.
frame = cv2.imread('./testData/CHNvsKR-19.jpg')

x, y = frame.shape[0:2]
# frame = cv2.resize(frame, (int(y / 2), int(x / 2)))

cimg = frame.copy()
src = frame.copy()

cimg = cv2.medianBlur(cimg, 9)

hsv = cv2.cvtColor(cimg, cv2.COLOR_BGR2HSV)

cimg = cv2.inRange(hsv, np.array([102, 177, 177]), np.array([118, 255, 224]))

# kernel = np.ones((20, 20), np.uint8)

# cv2.imshow('frame', cimg)

# cimg = cv2.morphologyEx(cimg, cv2.MORPH_OPEN, kernel)
# cimg = cv2.morphologyEx(cimg, cv2.MORPH_CLOSE, kernel)
# cv2.imshow('frame1', cimg)

# cv2.waitKey(0)

# exit(0)

frame = cv2.Canny(cimg, 10, 250, 5)

frame = cv2.copyMakeBorder(frame, 100, 100, 100, 100,
                           cv2.BORDER_CONSTANT, value=[0, 0, 0])
src = cv2.copyMakeBorder(src, 100, 100, 100, 100,
                         cv2.BORDER_CONSTANT, value=[0, 0, 0])

while True:
    # Get HSV values from the GUI sliders.
    param1 = cv2.getTrackbarPos('dp', 'colorTest')
    param2 = cv2.getTrackbarPos('minDist', 'colorTest')
    param3 = cv2.getTrackbarPos('param1', 'colorTest')
    param4 = cv2.getTrackbarPos('param2', 'colorTest')
    param5 = cv2.getTrackbarPos('minRadius', 'colorTest')
    param6 = cv2.getTrackbarPos('maxRadius', 'colorTest')

    # Show the original image.
    cv2.imshow('frame', frame)

    # Blur methods available, comment or uncomment to try different blur methods.
    # frameBGR = cv2.GaussianBlur(frame, (7, 7), 0)
    # frameBGR = cv2.medianBlur(frameBGR, 7)
    # frameBGR = cv2.bilateralFilter(frameBGR, 15 ,75, 75)
    """kernal = np.ones((15, 15), np.float32)/255
    frameBGR = cv2.filter2D(frameBGR, -1, kernal)"""

    # Show blurred image.
    # cv2.imshow('blurred', frameBGR)

    # HSV (Hue, Saturation, Value).
    # Convert the frame to HSV colour model.
    # hsv = cv2.cvtColor(frameBGR, cv2.COLOR_BGR2HSV)

    # # HSV values to define a colour range.
    # colorLow = np.array([lowHue,lowSat,lowVal])
    # colorHigh = np.array([highHue,highSat,highVal])
    # mask = cv2.inRange(hsv, colorLow, colorHigh)
    # # Show the first mask
    # cv2.imshow('mask-plain', mask)

    # kernal = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    # mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernal)
    # mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernal)

    # # Show morphological transformation mask
    # cv2.imshow('mask', mask)

    # Put mask over top of the original image.
    # result = cv2.bitwise_and(frame, frame, mask=mask)
    circles = cv2.HoughCircles(frame, cv2.HOUGH_GRADIENT, param1, param2, param1=param3, param2=param4,
                               minRadius=param5, maxRadius=param6)

    img = src.copy()

    if not circles is None:

        # print(i)

        for circle in circles[0]:
            # get the center and radius of the circle
            x, y, r = circle
            x = int(x)
            y = int(y)
            r = int(r)
            # draw the circle center
            cv2.circle(img, (x, y), 3, (0, 255, 0), -1)
            # draw the circle outline
            cv2.circle(img, (x, y), r, (0, 0, 255), 2)

    # Show final output image
    cv2.imshow('colorTest', img)

    k = cv2.waitKey(10) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
