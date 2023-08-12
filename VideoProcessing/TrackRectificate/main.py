import cv2
import numpy as np
from rich import print
from tsmoothie.utils_func import sim_randomwalk
from tsmoothie.smoother import LowessSmoother, DecomposeSmoother
import matplotlib.pyplot as plt
import easydict
from sklearn.neighbors import LocalOutlierFactor


class rectificate:
    def find(oimg):

        HOMO_COLOR = 114
        _, img = cv2.threshold(oimg, 127, 255, cv2.THRESH_BINARY)

        l, r = 0, 0
        bl, br = 0, 0
        mask = np.zeros([img.shape[0] + 2, img.shape[1] + 2], np.uint8)
        cv2.floodFill(img, mask, (img.shape[1] // 5 * 2, 0),
                      (HOMO_COLOR, HOMO_COLOR, HOMO_COLOR),
                      (0, 0, 0), (0, 0, 0), cv2.FLOODFILL_FIXED_RANGE)
        cv2.floodFill(img, mask, (img.shape[1] // 5 * 3, 0),
                      (HOMO_COLOR, HOMO_COLOR, HOMO_COLOR),
                      (0, 0, 0), (0, 0, 0), cv2.FLOODFILL_FIXED_RANGE)
        cv2.floodFill(img, mask, (img.shape[1] // 5 * 2, img.shape[0] - 1),
                      (HOMO_COLOR, HOMO_COLOR, HOMO_COLOR),
                      (0, 0, 0), (0, 0, 0), cv2.FLOODFILL_FIXED_RANGE)
        cv2.floodFill(img, mask, (img.shape[1] // 5 * 3, img.shape[0] - 1),
                      (HOMO_COLOR, HOMO_COLOR, HOMO_COLOR),
                      (0, 0, 0), (0, 0, 0), cv2.FLOODFILL_FIXED_RANGE)
        # cv2.imshow("vedio3", img)

        #
        for x in range(img.shape[1] - 1, img.shape[1] // 2, -1):
            pix = img[0, x]
            if (pix[0] == HOMO_COLOR and pix[1] == HOMO_COLOR and pix[2] == HOMO_COLOR):
                r = x
                break

        for x in range(0, img.shape[1] // 2):
            pix = img[0, x]
            if (pix[0] == HOMO_COLOR and pix[1] == HOMO_COLOR and pix[2] == HOMO_COLOR):
                l = x
                break

        for x in range(img.shape[1] - 1, img.shape[1] // 2, -1):
            pix = img[img.shape[0] - 1, x]
            if (pix[0] == HOMO_COLOR and pix[1] == HOMO_COLOR and pix[2] == HOMO_COLOR):
                br = x
                break

        for x in range(0, img.shape[1] // 2):
            pix = img[img.shape[0] - 1, x]
            if (pix[0] == HOMO_COLOR and pix[1] == HOMO_COLOR and pix[2] == HOMO_COLOR):
                bl = x
                break

        bl = (bl, img.shape[0] - 1)
        br = (br, img.shape[0] - 1)
        if (bl[0] == 0):
            bl = 0
            for x in range(img.shape[0] - 1, 0, -1):
                if (img[x, 0][0] != HOMO_COLOR or img[x, 0][1] != HOMO_COLOR or img[x, 0][2] != HOMO_COLOR):
                    bl = x
                    break
            bl = (0, bl)
        if (br[0] == img.shape[1] - 1):
            br = img.shape[1] - 1
            for x in range(img.shape[0] - 1, 0, -1):
                if (img[x, img.shape[1] - 1][0] != HOMO_COLOR or img[x, img.shape[1] - 1][1] != HOMO_COLOR or img[x, img.shape[1] - 1][2] != HOMO_COLOR):
                    br = x
                    break
            br = (img.shape[1], br)
        l = (l, 0)
        r = (r, 0)
        # print("find", l, r, bl, br);
        cv2.circle(img, l, 3, (0, 0, 255), 3)
        cv2.circle(img, r, 3, (0, 0, 255), 3)
        cv2.circle(img, bl, 3, (0, 0, 255), 3)
        cv2.circle(img, br, 3, (0, 0, 255), 3)
        cv2.line(img, l, bl, (0, 0, 255), 3)
        cv2.line(img, r, br, (0, 0, 255), 3)

        # img, tl, tr, bl, br
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
    cap = cv2.VideoCapture('../../videos/target2.tiny.mp4')
    
    if cap.isOpened():
        res = []
        data = []

        status = 0

        for i in range(0):  # 1900
            cap.grab()

        with tqdm(total=cap.get(7)) as pbar:
            while True:
                ret, img = cap.read()
                if (not ret):
                    break

                h, w = img.shape[:2]

                isScene, _ = SceneClassification(img)

                if isScene:

                    if status == 2:
                        res.append({
                            "type": 2,
                            "data": data
                        })
                        data = []

                    status = 1

                    img2, tl, tr, bl, br = rectificate.find(img)
                    cv2.imshow("video1", rectificate.trans(img2, tl, tr, bl, br))

                    key = cv2.waitKey(0)
                    if key == 113:
                        break

                    data.append([tl, tr, bl, br])

                else:

                    if status == 1:
                        res.append({
                            "type": 1,
                            "data": data
                        })
                        data = []

                    status = 2

                    cv2.imshow("video1", img)
                    data.append([(0, 0), (w, 0), (h, 0), (w, h)])

                    key = cv2.waitKey(0)
                    if key == 113:
                        break
                pbar.update(1)

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