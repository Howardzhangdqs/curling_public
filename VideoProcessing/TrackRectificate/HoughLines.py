import cv2
import numpy as np
from rich import print
from tsmoothie.utils_func import sim_randomwalk
from tsmoothie.smoother import LowessSmoother, DecomposeSmoother
import matplotlib.pyplot as plt
import easydict
from sklearn.neighbors import LocalOutlierFactor


class rectificate:
    def find(frame):

        frame = frame.copy()

        x, y = frame.shape[0:2]
        # frame = cv2.resize(frame, (int(y / 2), int(x / 2)))

        cimg = frame.copy()
        src = frame.copy()

        # cimg = cv2.medianBlur(cimg, 9)

        hsv = cv2.cvtColor(cimg, cv2.COLOR_BGR2HSV)

        cimg = cv2.inRange(hsv, np.array([46, 0, 164]), np.array([186, 91, 255]))
        
        kernel = np.ones((20, 20), np.uint8)
        cimg = cv2.morphologyEx(cimg, cv2.MORPH_CLOSE, kernel)

        cv2.imshow('imggg', cimg)

        frame = cv2.Canny(cimg, 10, 250, 5)

        kernel = np.ones((4, 4), np.uint8)
        frame = cv2.dilate(frame, kernel, 1)

        
        lines = cv2.HoughLinesP(frame, 1, np.pi / 180, 100, 200, 300)

        img = src.copy()

        if not lines is None:

            for i in lines:
                print(i)
                x1, y1, x2, y2 = i[0]
                cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)

        # img, tl, tr, bl, br
        l, r, bl, br = 0, 0, 0, 0
        
        # cv2.imshow('img', img)
        return img, l, r, bl, br

    def expand(shape, tl, tr, bl, br):
        tl, tr = tl[0], tr[0]
        if (bl[1] != shape[0] - 1):
            bl = bl[1]
            bl = - (shape[0] - bl) * tl // bl
            bl = (bl, shape[0])
        if (br[1] != shape[0] - 1):
            br = br[1]
            br = shape[1] + (shape[0] - br) * (shape[1] - tr) // br
            br = (br, shape[0])
        # print("expand", br, bl);
        return bl, br

    def trans(oimg, tl, tr, bl, br):
        # print(oimg.shape);
        points1 = np.float32([list(tl), list(tr), list(bl), list(br)])
        points2 = np.float32([[0, 0], [oimg.shape[1], 0], [0, oimg.shape[0]], [
                             oimg.shape[1], oimg.shape[0]]])
        M = cv2.getPerspectiveTransform(points1, points2)
        img = cv2.warpPerspective(oimg, M, (oimg.shape[1], oimg.shape[0]))
        return img


def SceneClassification(img):
    img = img.copy()

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array([46, 0, 164]), np.array([186, 91, 255]))

    cv2.imshow("mask1", mask)

    _mask = np.zeros([img.shape[0]+2, img.shape[1]+2], np.uint8)

    cv2.floodFill(mask, _mask, (0, 0), 0,
                  0, 0, cv2.FLOODFILL_FIXED_RANGE)

    cv2.floodFill(mask, _mask, (10, 10), 0,
                  0, 0, cv2.FLOODFILL_FIXED_RANGE)

    cv2.imshow("mask2", mask)

    mean = cv2.mean(mask)[0]
    # print(mean)

    if (mean > 110):
        return True, mean

    return False, mean

if __name__ == "__main__":
    from tqdm import *
    from sklearn.covariance import EllipticEnvelope
    cap = cv2.VideoCapture('../../videos/final1.mp4')
    
    if cap.isOpened():
        res = []
        data = []

        status = 0

        for i in range(0):  # 1900
            cap.grab()

        while True:
            ret, img = cap.read()
            if (not ret):
                break

            h, w = img.shape[:2]

            isScene, _ = SceneClassification(img)

            img2, tl, tr, bl, br = rectificate.find(img)
            cv2.imshow("video1", img2)

            key = cv2.waitKey(1)
            if key == 113:
                break

        print(res)

        data = []

        ans = []

        for item in res:
            tempdata = {
                "tl": {
                    "x": [],
                    "y": []
                },
                "tr": {
                    "x": [],
                    "y": []
                },
                "bl": {
                    "x": [],
                    "y": []
                },
                "br": {
                    "x": [],
                    "y": []
                }
            }

            # tempdata = easydict.EasyDict(tempdata)
            for val in item["data"]:
                tempdata["tl"]["x"].append(val[0][0])
                tempdata["tl"]["y"].append(val[0][1])

                tempdata["tr"]["x"].append(val[1][0])
                tempdata["tr"]["y"].append(val[1][1])
                
                tempdata["bl"]["x"].append(val[2][0])
                tempdata["bl"]["y"].append(val[2][1])
                
                tempdata["br"]["x"].append(val[3][0])
                tempdata["br"]["y"].append(val[3][1])

            ans.append({
                "type": item["type"],
                "data": tempdata
            })
        
        print(ans)