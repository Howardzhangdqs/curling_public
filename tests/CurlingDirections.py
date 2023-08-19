import os
import sys
import cv2
import yolov7_package
import BezierCurve
import random

os.environ["PROJECT_PATH"] = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../"))

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../")))

try:
    import VideoProcessing
    import TargetDetection
except:
    print("Error")


if __name__ == "__main__":
    cap = cv2.VideoCapture('../videos/target2.tiny.mp4')

    TargetDetection = TargetDetection.TargetDetection(device="cuda:0")

    if cap.isOpened():

        # for i in range(400):
        #     cap.grab()

        i = 0

        while True:

            ret, img = cap.read()
            if (not ret):
                break

            h, w = img.shape[:2]

            isScene, _ = VideoProcessing.SceneClassification(img)

            if isScene:

                i += 0.2

                img = VideoProcessing.SceneRectificate(img)

                line, _ = TargetDetection.insiderEdge(img)

                circle, _ = TargetDetection.camp(img)

                boxes, _, classes, img_curling = TargetDetection.curling(
                    img, threshold=0.7)
                print(boxes)

                if not circle is None:
                    cv2.circle(
                        img_curling, (circle[0], circle[1]), circle[2], (0, 255, 0), 5)

                if not line is None:
                    cv2.line(img_curling, (0, int(line)),
                             (w, int(line)), (0, 255, 0), 5)

                cv2.imshow("img", img_curling)

                if not len(boxes) == 0 and not circle is None:
                    print(boxes, circle)
                    cv2.imshow("img3", TargetDetection.GetBattleGroundPos(
                        img_curling.shape[1], img_curling.shape[0], circle, boxes, classes))

                try:
                    cv2.imshow("curling", cv2.resize((img[int(boxes[0][1]):int(boxes[0][3]), int(
                        boxes[0][0]):int(boxes[0][2])]), None, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC))
                except:
                    pass

                cv2.imshow("prediction", BezierCurve.DrawOnBattleGround([(885, 50), (200, random.randint(55 - int(50 / i), 60 + int(50 / i))), (150, random.randint(
                    50 - int(50 / i), 50 + int(50 / i)))]))

                key = cv2.waitKey(1)
                if key == 113:
                    break

            else:
                i = 0
                cv2.imshow("img", img)
                key = cv2.waitKey(1)
                if key == 113:
                    break
