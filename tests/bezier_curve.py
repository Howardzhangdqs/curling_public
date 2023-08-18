# 一个函数绘制塞贝尔曲线，给出四个关键点和一个cv2图片，返回绘制好的图片
def draw_bezier_curve(img, points, color=(0, 0, 255), thickness=2):
    for i in range(len(points) - 1):
        cv2.line(img, points[i], points[i + 1], color, thickness)
    return img