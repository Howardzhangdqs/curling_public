import os, sys, cv2
import yolov7_package

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
    
# draw bezier_curve using cv2
def draw_bezier_curve(img, points, color=(0, 0, 255), thickness=2):
    for i in range(len(points) - 1):
        cv2.line(img, points[i], points[i + 1], color, thickness)
    

    
if __name__ == "__main__":
    cap = cv2.VideoCapture('../videos/target2.tiny.mp4')


    TargetDetection = TargetDetection.TargetDetection()

    if cap.isOpened():

        # for i in range(400):
        #     cap.grab()

        while True:
            ret, img = cap.read()
            if (not ret):
                break

            h, w = img.shape[:2]

            isScene, _ = VideoProcessing.SceneClassification(img)

            if isScene:

                img = VideoProcessing.SceneRectificate(img)
                # print(TargetDetection.curling(img))

                line, _ = TargetDetection.insiderEdge(img)

                circle, _ = TargetDetection.camp(img)

                _, _, _, img_curling = TargetDetection.curling(img, threshold=0.7)

                if not line is None:
                    cv2.line(img_curling, (0, int(line)), (w, int(line)), (0, 255, 0), 5)

                if not circle is None:
                    cv2.circle(img_curling, (circle[0], circle[1]), circle[2], (0, 255, 0), 5)

                cv2.imshow("img", img_curling)
                cv2.imshow("curling", img_curling)

                key = cv2.waitKey(1)
                if key == 113:
                    break

            else:
                cv2.imshow("img", img)
                key = cv2.waitKey(1)
                if key == 113:
                    break