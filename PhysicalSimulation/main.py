import pymunk
import cv2
import random
import sys
import os

global Ball1Pos, Ball2Pos


def main(moving, speed, static, color):

    global Ball1Pos, Ball2Pos

    # 创建一个空间对象，设置重力为零
    space = pymunk.Space()
    space.gravity = 0, 0

    CurlingSize = 8

    def getRandomPos():
        return (random.randint(60, 220), random.randint(400, 580))

    Ball1Init = moving or (random.randint(80, 200), 300)
    Ball2Init = static or [getRandomPos() for i in range(3)]

    # Ball2Init = [(121, 312), (130, 354), (76, 410), (138, 445)]

    # [(121, 312), (130, 354), (76, 410), (138, 445)]

    # 创建两个圆形刚体对象，分别表示运动的球和静止的球
    ball1 = pymunk.Body(1, 10)  # 设置质量为1，惯性矩为10
    ball1.position = Ball1Init  # 设置初始位置为(100, 100)

    ball2 = []

    for i in Ball2Init:
        ballTemp = pymunk.Body(1, 10)  # 设置质量为1，惯性矩为10
        ballTemp.position = i  # 设置初始位置为(300, 100)
        ballTemp.inertia = 0.5
        ball2.append(ballTemp)

    # 创建两个圆形形状对象，分别与刚体对象关联
    shape1 = pymunk.Circle(ball1, CurlingSize)  # 设置半径为20

    shape2 = []

    for i in ball2:
        shapeTemp = pymunk.Circle(i, CurlingSize)  # 设置半径为20
        shape2.append(shapeTemp)
        space.add(i, shapeTemp)

    # 将形状对象添加到空间对象中
    space.add(ball1, shape1)

    def getRandomColor():
        t = random.randint(0, 1)
        return ((0, 0, 255), (0, 0, 255)) if t == 0 else ((255, 255, 0), (0, 255, 255))

    # 给运动的球一个初始速度，使其朝向静止的球运动
    ball1.velocity = speed or (random.randint(-20, 20), 200)
    shape1.elasticity = 0.8

    for i in shape2:
        i.elasticity = 0.8

    # 创建一个仿真步长，表示每次更新的时间间隔
    dt = 0.01

    # 创建一个黑色的背景图像，大小为400x200
    src = cv2.imread("black.png")

    cv2.imshow("Simulation", src)

    Ball1Pos = Ball1Init
    Ball2Pos = Ball2Init

    ballColor = color or [getRandomColor() for i in Ball2Init]

    def printXY(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print(x, y)

    cv2.setMouseCallback('Simulation', printXY)

    def render():

        global Ball1Pos, Ball2Pos

        Ball1CurrentPos = (int(ball1.position.x), int(ball1.position.y))
        Ball2CurrentPos = []

        for i, j, k, l in zip(Ball2Init, ball2, Ball2Pos, ballColor):
            t = (int(j.position.x), int(j.position.y))
            Ball2CurrentPos.append(t)
            cv2.circle(img, t, CurlingSize, l[1], -1)
            cv2.circle(img, t, CurlingSize, (0, 0, 0), 2)
            cv2.line(src, k, t, l[0], 2)

        # 在图像上绘制两个球的位置，颜色为白色，线宽为-1（表示填充）
        cv2.circle(img, Ball1CurrentPos, CurlingSize, (0, 0, 255), -1)
        cv2.circle(img, Ball1CurrentPos, CurlingSize, (0, 0, 0), 2)

        cv2.line(src, Ball1Pos, Ball1CurrentPos, (0, 0, 255), 2)

        Ball1Pos = Ball1CurrentPos
        Ball2Pos = Ball2CurrentPos

        # 显示图像，并等待10毫秒的按键
        cv2.imshow("Simulation", img)


    waitKey = 1

    out = cv2.VideoWriter('out.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 60, (src.shape[1], src.shape[0]))

    # 循环更新空间对象，模拟物理运动
    for i in range(300):
        img = src.copy()

        for i in range(1):
            space.step(dt)

        render()
        out.write(img)

        key = cv2.waitKey(int(waitKey))

        waitKey *= 1.01

        print(key)

        while key == 112:
            ballColor = [getRandomColor() for i in Ball2Init]
            render()
            key = cv2.waitKey(0)
        
        if key == 113:
            break
        if key == 114:
            exit(0)
        
    out.release()


def label2color(label):
    res = []
    for i in label:
        if (i == 1):
            res.append(((0, 0, 255), (0, 0, 255)))
        else:
            res.append(((255, 255, 0), (0, 255, 255)))
    
    return res


main(moving=(100, 200),
     speed=(0, 200),
     static=[(112, 441), (76, 436), (60, 475), (106, 575), (74, 541), (83, 360)],
     color=label2color([2, 1, 2, 2, 1, 2]))
