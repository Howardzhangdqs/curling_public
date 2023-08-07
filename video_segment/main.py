from option import OPT
import os
import sys
import cv2
import numpy as np
from typing import List

from rich import print


def getCurrentState_color(frame) -> List:

    hsv = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2Lab)
    # hsv = frame.copy()

    res: List = [[], []]

    ver: int = OPT.STATE_VERTICAL

    offset: int = OPT.STATE_OFFSET

    for i in OPT.STATE_POSITION:

        part1 = hsv[ver[0] - 5: ver[0] + 5, i - 5: i + 5]
        part2 = hsv[ver[1] - 5: ver[1] + 5, i - 5: i + 5]

        part1 = np.average(np.average(part1, axis=0), axis=0)
        part2 = np.average(np.average(part2, axis=0), axis=0)

        print(part1, part2)

        part1 = part1.tolist()
        part2 = part2.tolist()

        frame[ver[0] - offset: ver[0] + offset, i - offset: i +
              offset] = cv2.cvtColor(np.uint8([[part1]]), cv2.COLOR_Lab2BGR)[0][0]
        frame[ver[1] - offset: ver[1] + offset, i - offset: i +
              offset] = cv2.cvtColor(np.uint8([[part2]]), cv2.COLOR_Lab2BGR)[0][0]

        res[0].append(part1)
        res[1].append(part2)

    if OPT.debug:
        for i in OPT.STATE_POSITION:
            frame[ver[0], i] = [0, 0, 255]
            frame[ver[1], i] = [0, 0, 255]

    # 203 38
    # print(res)

    return res


def getCurrentState_merge(color: List):
    res: List = color.copy()

    for j, items in enumerate(color[0]):
        res[0][j] = True

        for i, item in enumerate(items):
            if (not item in OPT.CurlingInterval_red[i]):
                res[0][j] = False

    for j, items in enumerate(color[1]):
        res[1][j] = True

        for i, item in enumerate(items):
            if (not item in OPT.CurlingInterval_yel[i]):
                res[1][j] = False

    return res


def getCurrentState_filter(state: List):
    res1 = 0
    res2 = 0

    for i, item in enumerate(state[0]):
        if (item == False):
            res1 = i
            break

    for i, item in enumerate(state[1]):
        if (item == False):
            res2 = i
            break

    return (res1, res2)


def getCurrentState(frame):
    return getCurrentState_merge(getCurrentState_color(frame))

if __name__ == '__main__':

    cap = cv2.VideoCapture(OPT.VIDEO_PATH)

    if not cap.isOpened():
        print("无法打开视频文件")

    for i in range(701 + 2320):
        cap.grab()

    i: int = 0

    while True:

        # 读取帧
        ret, frame = cap.read()

        # 检查是否成功读取帧
        if not ret:
            break

        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        i += 1

        # print((
        #     getCurrentState(getCurrentState_color(frame))))
        # getCurrentState_filter(getCurrentState(getCurrentState_color(frame)))

        t = getCurrentState_merge(getCurrentState_color(frame))

        # result = [subarr[:-1] for subarr in t[:2]]
        # result = [subarr[:-1] for subarr in result[:2]]
        print(i, t)

        if (i % 100 == 0):
            print(i)

        # if (not all(result[0]) or not all(result[1])):
        #     print(i, result)
        #     cv2.imshow('frame', frame)
        #     cv2.waitKey(0)
        #     # exit(0)

        # 显示帧
        # cv2.imshow('frame', frame)

        # 按下q键退出
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

    # 释放
    cap.release()
    cv2.destroyAllWindows()
