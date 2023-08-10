import cv2
import numpy as np
from rich import print


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

    mean = cv2.mean(mask)[0]
    print(mean, end=" ")


    if (mean > 100):
        return True, mean

    return False, mean


# if __name__ == "__main__":
#     for i in range(1, 5):
#         frame = cv2.imread(f"./testData/{i}.png")
#         SceneClassification(frame)

# exit(0)

if __name__ == "__main__":
    from tqdm import *
    from sklearn.covariance import EllipticEnvelope
    cap = cv2.VideoCapture('../../videos/target2.tiny.mp4')
    # out = cv2.VideoWriter('output.mp4',
    #                       cv2.VideoWriter_fourcc(*'mp4v'),
    #                       cap.get(cv2.CAP_PROP_FPS),
    #                       (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
    if cap.isOpened():
        data = []

        for i in range(200):
            cap.grab()

        with tqdm(total=cap.get(7)) as pbar:
            while True:
                ret, img = cap.read()
                if (not ret):
                    break

                h, w = img.shape[:2]

                isScene, _ = SceneClassification(img)

                if isScene:

                    img2, tl, tr, bl, br = rectificate.find(img)
                    # bl, br = rectificate.expand(img.shape, tl, tr, bl, br)
                    # img3 = rectificate.trans(img, tl, tr, bl, br)
                    cv2.imshow("video1", img2)
                    # cv2.imshow("video2", img)
                    # out.write(img3)
                    key = cv2.waitKey(1)
                    # print(key)
                    if key == 113:
                        break
                    data.append([tl, tr, bl, br])

                else:
                    cv2.imshow("video1", img)
                    data.append([(0, 0), (w, 0), (h, 0), (w, h)])
                    key = cv2.waitKey(1)
                # img3 = rectificate.trans(img, tl, tr, bl, br);
                # cv2.imshow("vedio1", img3)
                # cv2.imshow("vedio2", img)
                # cv2.waitKey(0);
                pbar.update(1)
        # out.release()
        ls = {
            "tl": {
                "x": [i[0][0] for i in data],
                "y": [i[0][1] for i in data]
            },
            "tr": {
                "x": [i[1][0] for i in data],
                "y": [i[1][1] for i in data]
            },
            "bl": {
                "x": [i[2][0] for i in data],
                "y": [i[2][1] for i in data]
            },
            "br": {
                "x": [i[3][0] for i in data],
                "y": [i[3][1] for i in data]
            }
        }
        # ls["tl"] = [i[0] for i in data]
        # ls["tr"] = [i[1] for i in data]
        # ls["bl"] = [i[2] for i in data]
        # ls["br"] = [i[3] for i in data]
        print(ls)
        # predictions = EllipticEnvelope().fit(ls["tl"]).predict(ls["tl"])
        # print(predictions)
        # cap = cv2.VideoCapture('test2.mp4')
        # i = -1
        # while True:
        #     ret, img = cap.read()
        #     if (not ret):
        #         break
        #     i += 1
        #     tl, tr, bl, br = ls["tl"][i], ls["tr"][i], ls["bl"][i], ls["br"][i]
        #     img3 = rectificate.trans(img, tl, tr, bl, br)
        #     if (predictions[i] < 0):
        #         cv2.rectangle(
        #             img3, (0, 0), (img3.shape[0], img3.shape[1]), (0, 0, 255), 3)
        #     cv2.imshow("video1", img3)
        #     cv2.imshow("video2", img)
        #     cv2.waitKey(1)
