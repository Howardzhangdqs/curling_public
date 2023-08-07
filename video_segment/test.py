from main import getCurrentState
from option import OPT
import cv2

from rich import print

if __name__ == '__main__':

    cap = cv2.VideoCapture(OPT.VIDEO_PATH)

    if not cap.isOpened():
        print("无法打开视频文件")

    for i in range(1111):
        cap.grab()

    i: int = 0

    while True:

        # 读取帧
        ret, frame = cap.read()

        # 检查是否成功读取帧
        if not ret:
            break
        
        i += 1
        
        t = getCurrentState(frame)

        print(i, t)

        if (i % 100 == 0):
            print(i)

        cv2.imshow('frame', frame)

        if cv2.waitKey(0) & 0xFF == ord('q'):
            break

    # 释放
    cap.release()
    cv2.destroyAllWindows()
