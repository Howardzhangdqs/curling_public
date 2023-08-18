import cv2
import os
import sys
import numpy as np
from rich import print


os.environ["PROJECT_PATH"] = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../"))

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../")))
sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../")))

try:
    import VideoProcessing
except:
    VideoProcessing = object


def detect(img):
    img = img.copy()

    # img = VideoProcessing.SceneRectificate(img)

    # cv2.imshow("mask", img)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img = cv2.medianBlur(img, 7)
    mask = cv2.inRange(img, np.array(
        [167, 120, 194]), np.array([175, 224, 235]))

    # cv2.imshow("mask1", mask)

    # 膨胀再侵蚀
    kernel = np.ones((2, 150), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=1)
    # cv2.imshow("mask2.2", mask)
    mask = cv2.erode(mask, kernel, iterations=3)

    # cv2.imshow("mask2", mask)

    # 疯狂膨胀
    kernel = np.ones((1, 600), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=3)

    # cv2.imshow("mask3", mask)

    height = img.shape[0]

    # 统计
    res = []

    for row in range(height):
        if int(cv2.mean(mask[row])[0]) >= 250:
            res.append(row)
    
    if len(res) == 0:
        return None, None

    return (res[0] + res[len(res) - 1]) // 2, res


if __name__ == "__main__":
    img = cv2.imread("./testData/2.png")
    row, rows = detect(img)
    print(row, rows)

    cv2.waitKey(0)
