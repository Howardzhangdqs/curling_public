
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


icol = (2, 100, 0, 0, 0, 0)

cv2.namedWindow('colorTest')
# Lower range colour sliders.
cv2.createTrackbar('dp', 'colorTest', icol[0], 10, nothing)
cv2.createTrackbar('minDist', 'colorTest', icol[1], 1000, nothing)
cv2.createTrackbar('param1', 'colorTest', icol[2], 1000, nothing)
cv2.createTrackbar('param2', 'colorTest', icol[3], 1000, nothing)

# Raspberry pi file path example.
# frame = cv2.imread('/home/pi/python3/opencv/color-test/colour-circles-test.jpg')
# Windows file path example.
frame = cv2.imread('./testData/2.png')

x, y = frame.shape[0:2]
# frame = cv2.resize(frame, (int(y / 2), int(x / 2)))

cimg = frame.copy()
src = frame.copy()

# cimg = cv2.medianBlur(cimg, 9)

hsv = cv2.cvtColor(cimg, cv2.COLOR_BGR2HSV)

cimg = cv2.inRange(hsv, np.array([46, 0, 164]), np.array([186, 91, 255]))

cv2.imshow('cimg', cimg)

frame = cv2.Canny(cimg, 10, 250, 5)

kernel = np.ones((4, 4), np.uint8)
frame = cv2.dilate(frame, kernel, 1)

cv2.imshow('frame', frame)

while True:
    # Get HSV values from the GUI sliders.
    param1 = cv2.getTrackbarPos('dp', 'colorTest')
    param2 = cv2.getTrackbarPos('minDist', 'colorTest')
    param3 = cv2.getTrackbarPos('param1', 'colorTest')
    param4 = cv2.getTrackbarPos('param2', 'colorTest')

    # Show the original image.

    # Blur methods available, comment or uncomment to try different blur methods.
    # frameBGR = cv2.GaussianBlur(frame, (7, 7), 0)
    # frameBGR = cv2.medianBlur(frameBGR, 7)
    # frameBGR = cv2.bilateralFilter(frameBGR, 15 ,75, 75)
    """kernal = np.ones((15, 15), np.float32)/255
    frameBGR = cv2.filter2D(frameBGR, -1, kernal)"""

    lines = cv2.HoughLinesP(frame, 1, np.pi / 180, 100, param3, param4)

    img = src.copy()

    if not lines is None:

        for i in lines:
            print(i)
            x1, y1, x2, y2 = i[0]
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)

    # Show final output image
    cv2.imshow('colorTest', img)

    k = cv2.waitKey(10) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
