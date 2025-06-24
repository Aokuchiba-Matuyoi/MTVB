import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import os

dir_path = "FREE"
for filename in os.listdir(dir_path):
    file_path = os.path.join(dir_path, filename)
    mtvb = cv.imread(file_path, 0)
    ret, mtvb = cv.threshold(mtvb, 15, 255, cv.THRESH_BINARY_INV)
    cv.imwrite(file_path, mtvb)