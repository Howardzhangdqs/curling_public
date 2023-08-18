# 导入cv2和numpy模块
import cv2
import numpy as np

# 定义一个贝塞尔曲线的函数
def BezierCurve(points, t):
    # 获取控制点的个数
    n = len(points) - 1
    # 初始化曲线上的点坐标
    x = 0
    y = 0
    # 遍历每个控制点，计算其对曲线上的点坐标的贡献
    for i in range(n + 1):
        # 计算组合数C(n, i)
        c = 1
        for j in range(i + 1, n + 1):
            c *= j
        for j in range(1, n - i + 1):
            c //= j
        # 计算贝塞尔基函数B(n, i, t)
        b = c * (t ** i) * ((1 - t) ** (n - i))
        # 累加控制点的坐标乘以贝塞尔基函数
        x += points[i][0] * b
        y += points[i][1] * b
    # 返回曲线上的点坐标，取整为整数
    return int(x), int(y)

# 定义一个绘制贝塞尔曲线的函数
def DrawBezierCurve(points, img):
    # 定义一个参数序列，从0到1，步长为0.01
    t = np.arange(0, 1.01, 0.01)
    # 定义一个空列表，用于存储曲线上的点坐标
    curve = []
    # 遍历每个参数值，使用贝塞尔曲线函数计算曲线上的点坐标，并添加到列表中
    for ti in t:
        curve.append(BezierCurve(points, ti))
    # 将列表转换为numpy数组，方便后续操作
    curve = np.array(curve)
    # 使用cv2.polylines函数在图像上绘制贝塞尔曲线，颜色为蓝色，粗细为2
    cv2.polylines(img, [curve], False, (255, 0, 0), 2)
    # 返回绘制好的图片对象
    return img

def DrawOnBattleGround(points):
    img = cv2.imread("battleground.min.png")
    # 创建一个空白的图像，大小为300x300，颜色为白色
    img = cv2.resize(img, None, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)
    img = DrawBezierCurve(points, img)
    return img

if __name__ == "__main__":
    points = [(885, 55), (200, 60), (150, 50)]

    # 调用draw_bezier_curve函数，传入控制点和图片作为参数，得到绘制好的图片对象
    img = DrawBezierCurve(points, img)

    # 使用cv2.imshow函数显示图片
    cv2.imshow("Cat with Bezier Curve", img)

    # 等待用户按任意键关闭窗口
    cv2.waitKey(0)