import cv2 as cv
import numpy as np
kernel = np.ones((3, 3), np.uint8)
image_result = cv.imread("result/0.23.jpg", 0) # 0 255赋值
for x in range(3):
    image_result = cv.erode(image_result, kernel, 1) # 腐蚀操作
cv.imwrite("result/0.24.jpg", image_result)

ret, image_result = cv.threshold(image_result, 5, 255, cv.THRESH_BINARY_INV)


for x in range(20):
    image_result = cv.erode(image_result, kernel, 1) # 腐蚀操作
cv.imwrite("result/0.25.jpg", image_result)
for x in range(20):
    image_result = cv.dilate(image_result, kernel, 1)  # 膨胀操作
cv.imwrite("result/0.26.jpg", image_result)