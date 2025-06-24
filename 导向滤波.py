import numpy as np
import cv2
import os

src = cv2.imread("images_in_the_paper/dolam_3.jpg", 0)
# src = cv2.imread("images_in_the_paper/dolam_2.jpg", 0)
guide = src

def guideFilter(I, p, winSize, eps):

    mean_I = cv2.blur(I, winSize)      # I的均值平滑
    mean_p = cv2.blur(p, winSize)      # p的均值平滑

    mean_II = cv2.blur(I * I, winSize) # I*I的均值平滑
    mean_Ip = cv2.blur(I * p, winSize) # I*p的均值平滑

    var_I = mean_II - mean_I * mean_I  # 方差
    cov_Ip = mean_Ip - mean_I * mean_p # 协方差

    a = cov_Ip / (var_I + eps)         # 相关因子a
    b = mean_p - a * mean_I            # 相关因子b

    mean_a = cv2.blur(a, winSize)      # 对a进行均值平滑
    mean_b = cv2.blur(b, winSize)      # 对b进行均值平滑

    q = mean_a * I + mean_b
    return q

def subtract(origin, modify):
    if isinstance(origin, np.ndarray) and isinstance(modify, np.ndarray):
        h1, w1 = origin.shape[:2]
        h2, w2 = modify.shape[:2]

        # 判断宽高是否相同
        if w1 == w2 and h1 == h2:
            print("两张图片大小相同")
            modify = modify - origin
            return modify
        else:
            print("大小不同")
            return 0
    else:
        return 0

if __name__ == '__main__':
    dir_path = "Guide"
    first = 1
    second = 1
    count = 1
    eps = 0.01
    winSize = (5, 5)
    for filename in os.listdir(dir_path):
        # 拼接文件路径
        file_path = os.path.join(dir_path, filename)
        first = int(filename.split(".")[0])
        second = int(filename.split(".")[1])
        if second == 1:
            first_time = False
            origin = cv2.imread(file_path, 0)
            print("获得原图")


        else:
            guide = cv2.imread(file_path, 0)
            print("获得导向图")
            src = subtract(origin, guide)
            if type(src) == int:
                os.remove(file_path)
            else:
                path = dir_path + "/" + str(first) + "." + str(second) + "." + "1.jpg"
                cv2.imwrite(path, src)
                try:
                    # 保存导向滤波结果
                    guideFilter_img = guideFilter(guide, src, winSize, eps)
                    path = dir_path + "/" + str(first) + "." + str(second) + "." + "2.jpg"
                    guideFilter_img = guideFilter_img * 255
                    guideFilter_img[guideFilter_img > 255] = 255
                    guideFilter_img = np.round(guideFilter_img)
                    guideFilter_img = guideFilter_img.astype(np.uint8)
                    cv2.imwrite(path, guideFilter_img)
                except:
                    pass
            # 保存导向滤波结果



