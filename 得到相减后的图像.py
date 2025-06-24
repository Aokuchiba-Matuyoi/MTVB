import cv2 as cv
import numpy as np

def subtract(origin, modify):
    h1, w1 = origin.shape[:2]
    h2, w2 = modify.shape[:2]

    # 判断宽高是否相同
    if w1 == w2 and h1 == h2:
        print("两张图片大小相同")
        result = modify - origin
        return result
    else:
        print("大小不同")
        return 0

a = cv.imread("FREE/2.1.jpg", 0)
b = cv.imread("FREE/2.2.jpg", 0)
result = subtract(a, b)

# 将像素值低于30的部分置为0
point = 10
result[result < point] = 0
result[result >= point] = 255

cv.imwrite("FREE/substract_Gaussian.jpg", result)
