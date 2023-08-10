from option import OPT as option
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

    ver: int = option.STATE_VERTICAL

    offset: int = option.STATE_OFFSET

    for i in option.STATE_POSITION:

        part1 = hsv[ver[0] - 5: ver[0] + 5, i - 5: i + 5]
        part2 = hsv[ver[1] - 5: ver[1] + 5, i - 5: i + 5]

        part1 = np.average(np.average(part1, axis=0), axis=0)
        part2 = np.average(np.average(part2, axis=0), axis=0)

        # print(part1, part2)

        part1 = part1.tolist()
        part2 = part2.tolist()

        frame[ver[0] - offset: ver[0] + offset, i - offset: i +
              offset] = cv2.cvtColor(np.uint8([[part1]]), cv2.COLOR_Lab2BGR)[0][0]
        frame[ver[1] - offset: ver[1] + offset, i - offset: i +
              offset] = cv2.cvtColor(np.uint8([[part2]]), cv2.COLOR_Lab2BGR)[0][0]

        res[0].append(part1)
        res[1].append(part2)

    if option.debug:
        for i in option.STATE_POSITION:
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
            if (not item in option.CurlingInterval_red[i]):
                res[0][j] = False

    for j, items in enumerate(color[1]):
        res[1][j] = True

        for i, item in enumerate(items):
            if (not item in option.CurlingInterval_yel[i]):
                res[1][j] = False

    return res


def getCurrentState_filter(state: List):
    res1, res2 = 0, 0

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


def FlattenList(nested_list):
    flattened_list = []
    for item in nested_list:
        if isinstance(item, list):
            flattened_list.extend(FlattenList(item))
        else:
            flattened_list.append(item)
    return flattened_list


def BoolList2StringList(ls):
    res = []
    for i in ls:
        res.append("1" if i else "0")
    return res


if __name__ == '__main__':

    cap = cv2.VideoCapture(option.VIDEO_PATH)

    if not cap.isOpened():
        print("无法打开视频文件")
    
    # for i in range(1398):
    #     cap.grab()

    i: int = 0

    res = []

    while True:

        ret, frame = cap.read()
        if not ret:
            break

        i += 1

        t = getCurrentState(frame)
        print(i, t)

        res.append(" ".join(BoolList2StringList(FlattenList(t))))

        if (i >= 3200):
            break

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    file = open("./output/P1.txt", "w")
    file.write(str(len(res)) + "\n")
    file.write("\n".join(res))
    file.close()
