import cv2
import numpy as np


def process_image_cv2(image_path):
    # 使用cv2读取图像
    img = cv2.imread(image_path)

    # 找出所有不是(192, 192, 192)的像素位置
    mask = np.all(img != [192, 192, 192], axis=-1)

    # 将这些像素变为黑色
    img[mask] = [0, 0, 0]

    # 保存或显示处理后的图像
    cv2.imwrite('FREE/bb.png', img)  # 保存图像
    cv2.imshow('Processed Image', img)  # 显示图像
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# 调用函数处理图像
process_image_cv2('FREE/b.png')  # 使用实际的图像路径
