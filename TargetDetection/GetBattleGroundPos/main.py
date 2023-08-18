import os
import sys
import cv2
import random

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
    import TargetDetection
except:
    print("Error")

# 给出坐标的中心点，以及缩放比例，返回缩放后的坐标


def ScaleData(point, center, scale):
    return [(point[0] - center[0]) * scale, (point[1] - center[1]) * scale]


def Render(img, curlingPos, classes):
    for pos, cla in zip(curlingPos, classes):
        cv2.circle(img, (int(pos[0]), int(pos[1])), 8, (0, 0, 255) if cla == 0 else (0, 255, 255), -1)
        cv2.circle(img, (int(pos[0]), int(pos[1])), 8, (0, 0, 0), 2)
    # cv2.imshow("img2", img)
    # cv2.waitKey(0)

    return img

global background

background = cv2.imread(os.path.abspath(
    os.path.join(os.path.dirname(__file__), "./battleground.png")))

def getPos(w, h, circle, boxes, classes):

    global background

    print(circle, boxes, classes)

    curlingPos = []

    for box in boxes:
        curlingPos.append([(box[0] + box[2]) // 2, (box[1] + box[3]) // 2])

    offset = circle[0], circle[1]

    for index, val in enumerate(curlingPos):
        curlingPos[index][0] -= offset[0]
        curlingPos[index][1] -= offset[1]

        curlingPos[index] = ScaleData(
            curlingPos[index], (0, 0), 100 / circle[2])

        print(curlingPos[index])

        curlingPos[index][0] += 137
        curlingPos[index][1] += 503

    print(circle, boxes, curlingPos)


    return Render(background, curlingPos, classes)


if __name__ == "__main__":
    img = cv2.imread("./testData/target.png")

    TargetDetection = TargetDetection.TargetDetection()

    img = VideoProcessing.SceneRectificate(img)

    line, _ = TargetDetection.insiderEdge(img)

    circle, _ = TargetDetection.camp(img)

    boxes, _, classes, img = TargetDetection.curling(img, threshold=0.4)

    if not circle is None:
        cv2.circle(
            img, (circle[0], circle[1]), circle[2], (0, 255, 0), 5)

    cv2.imshow("img", img)

    img = getPos(img.shape[1], img.shape[0], circle, boxes, classes)

    cv2.imshow("img2", img)
    cv2.waitKey(0)
