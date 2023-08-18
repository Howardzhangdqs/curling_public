import cv2
import numpy as np
from rich import print
import uuid
import copy


ImgBroaden = 200


def DisplayFrame(img):
    cv2.imshow(uuid.uuid4().hex[:-6], img)
    cv2.waitKey(0)


def CampFind(frame):

    frame = frame.copy()
    x, y = frame.shape[0:2]

    cimg = frame.copy()
    src = frame.copy()

    # 对临时图像进行中值滤波
    cimg = cv2.medianBlur(cimg, 9)

    # 将临时图像从BGR颜色空间转换为HSV颜色空间
    hsv = cv2.cvtColor(cimg, cv2.COLOR_BGR2HSV)

    # 根据设定的颜色范围，将图像转换为二值图像
    cimg = cv2.inRange(hsv, np.array(
        [102, 177, 177]), np.array([118, 255, 224]))

    # 对二值图像进行边缘检测
    frame = cv2.Canny(cimg, 10, 250, 5)

    kernel = np.ones((4, 4), np.uint8)
    frame = cv2.dilate(frame, kernel, 1)

    # DisplayFrame(frame)

    # 对边缘检测结果进行边界填充，以避免边缘上的圆被截断
    frame = cv2.copyMakeBorder(
        frame, ImgBroaden, ImgBroaden, ImgBroaden, ImgBroaden, cv2.BORDER_CONSTANT, value=[0, 0, 0])
    src = cv2.copyMakeBorder(src, ImgBroaden, ImgBroaden, ImgBroaden, ImgBroaden,
                             cv2.BORDER_CONSTANT, value=[0, 0, 0])

    # 使用霍夫圆变换检测图像中的圆
    circles = cv2.HoughCircles(
        frame, cv2.HOUGH_GRADIENT, 2, 50, param1=100, param2=60, minRadius=0, maxRadius=0)

    # 在原始图像上绘制检测到的圆
    img = src.copy()

    _frame = frame.copy()
    _frame = cv2.cvtColor(_frame, cv2.COLOR_GRAY2BGR)

    # if not circles is None:
    #     for circle in circles[0]:
    #         x, y, r = circle
    #         x = int(x)
    #         y = int(y)
    #         r = int(r)
    #         cv2.circle(_frame, (x, y), 3, (0, 255, 0), -1)
    #         cv2.circle(_frame, (x, y), r, (0, 0, 255), 2)

    # cv2.imshow("video2", _frame)

    return circles, src, frame


def CampFilter(circle, src, canny):
    src = src.copy()
    canny = canny.copy()
    circle = copy.deepcopy(circle)[0]

    CannySize = canny.shape[0:2]

    kernel = np.ones((10, 10), np.uint8)
    canny = cv2.dilate(canny, kernel, 1)

    SrcMat = np.zeros(CannySize, np.uint8)
    SrcMat.fill(0)

    SrcMat = cv2.cvtColor(SrcMat, cv2.COLOR_GRAY2BGR)
    SrcMat = cv2.cvtColor(SrcMat, cv2.COLOR_BGR2GRAY)

    MaxMean, MaxCircle = 0.0, 0

    for index, i in enumerate(circle):
        x, y, r = i
        x = int(x)
        y = int(y)
        r = int(r)

        mat = SrcMat.copy()
        cv2.circle(mat, (x, y), r, (255), 1)

        img = (mat[:, :]) / 255. * (canny[:, :]) / 255.

        Mean = cv2.mean(img)[0]

        if (MaxMean < Mean):
            MaxMean = Mean
            MaxCircle = (x, y, r)

    circle = [MaxCircle]

    for i in range(40, 100, 5):
        circle.append((MaxCircle[0], MaxCircle[1], MaxCircle[2] + i))

    MaxMean, MaxCircle = 0.0, 0

    for index, i in enumerate(circle):
        x, y, r = i
        x = int(x)
        y = int(y)
        r = int(r)

        mat = SrcMat.copy()
        cv2.circle(mat, (x, y), r, (255), 1)

        img = (mat[:, :]) / 255. * (canny[:, :]) / 255.

        Mean = cv2.mean(img)[0]

        if (MaxMean < Mean):
            MaxMean = Mean
            MaxCircle = (x, y, r)

    return (MaxCircle[0] - ImgBroaden, MaxCircle[1] - ImgBroaden, MaxCircle[2]), mat, canny


def getCurrentCamp(frame):
    frame = frame.copy()

    circle, img, canny = CampFind(frame)
    
    if not circle is None:
        return CampFilter(circle, img, canny)

    return None, img, canny

if __name__ == '__main__':

    capture = cv2.VideoCapture(
        r"D:\DEV\Curling\curling_public\videos\target2.tiny.mp4")

    # 3 读取视频
    ret, frame = capture.read()

    for i in range(300):
        capture.grab()
    
    i = 300

    while ret:
        ret, frame = capture.read()
        src = frame.copy()

        i += 1

        circle, img, canny = getCurrentCamp(frame)
        # print(circle)

        if not circle is None:

            cv2.circle(frame, (circle[0], circle[1]), circle[2], (0, 255, 0), 5)

        cv2.imshow("video", frame)
        cv2.imshow("video_src", src)

        key = cv2.waitKey(1)

        if key & 0xff == ord(' '):
            print(i)
            cv2.waitKey(0)

        if key & 0xff == ord('q'):
            break

    # 4 释放资源
    capture.release()
