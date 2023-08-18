from yolov7_package import Yolov7Detector
import cv2
import os


class Detector():

    def __init__(self, device="cpu"):

        self.dirname = os.path.dirname(__file__)
        self.modelPath = os.path.abspath(os.path.join(
            self.dirname, "../../models/yolov7-tiny.pt"))
        self.classPath = os.path.abspath(os.path.join(
            self.dirname, "../../models/classes.txt"))

        print("ModelPath:", self.modelPath, " ClassPath:", self.classPath)
        self.det = Yolov7Detector(
            weights=self.modelPath, classes=self.classPath, traced=False, device=device)
        print("Model Loaded")

    def detect(self, img, threshold=0.3):

        img = img.copy()

        classes, boxes, scores = self.det.detect(img)
        boxes, scores, classes = boxes[0], scores[0], classes[0]

        # print(boxes, scores, classes)

        newBoxes, newScores, newClasses = [], [], []

        for box, score, cla in zip(boxes, scores, classes):
            if (score > threshold):
                newBoxes.append(box)
                newScores.append(score)
                newClasses.append(cla)

        # print(boxes, scores, classes)

        # img = self.det.draw_on_image(img, boxes, scores, classes)

        return newBoxes, newScores, newClasses, self.drawBox(img, newBoxes, newScores, newClasses)

    def drawBox(self, img, boxes, scores, classes):
        colors = [(0, 0, 255), (0, 0, 255), (0, 255, 255),
                  (0, 0, 255), (0, 0, 255)]
        img = img.copy()
        for box, score, cla in zip(boxes, scores, classes):
            cv2.rectangle(img, (int(box[0]), int(box[1])), (int(
                box[2]), int(box[3])), colors[cla], 2)
            cv2.putText(img, str(round(score, 4)), (int(box[0]), int(
                box[1] - 5)), cv2.FONT_HERSHEY_PLAIN, 1, colors[cla], 2)
        return img


if __name__ == "__main__":
    img = cv2.imread("./testData/Snipaste_2023-08-12_10-12-48.png")

    det = Detector()
    boxes, scores, classes, img = det.detect(img)
    cv2.imshow("img", img)
    cv2.waitKey(0)
