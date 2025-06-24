import cv2 as cv
import numpy as np

def gaussian_filter(img, K_size=99, sigma=20.0):
    img = np.asarray(np.uint8(img))
    if len(img.shape) == 3:
        H, W, C = img.shape
    else:
        img = np.expand_dims(img, axis=-1)
        H, W, C = img.shape

    ## Zero padding
    pad = K_size // 2
    out = np.zeros((H + pad * 2, W + pad * 2, C), dtype=float)
    out[pad: pad + H, pad: pad + W] = img.copy().astype(float)

    ## prepare Kernel
    K = np.zeros((K_size, K_size), dtype=float)
    for x in range(-pad, -pad + K_size):
        for y in range(-pad, -pad + K_size):
            K[y + pad, x + pad] = np.exp(-(x ** 2 + y ** 2) / (2 * (sigma ** 2)))
    K /= (2 * np.pi * sigma * sigma)
    K /= K.sum()
    tmp = out.copy()

    # filtering
    for y in range(H):
        for x in range(W):
            for c in range(C):
                out[pad + y, pad + x, c] = np.sum(K * tmp[y: y + K_size, x: x + K_size, c])
    out = np.clip(out, 0, 255)
    out = out[pad: pad + H, pad: pad + W].astype(np.uint8)
    return out

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

origin = 'IMG/28.1.jpg'
tamper = 'IMG/28.2.jpg'
image0 = cv.imread(origin, 0)
image0 = gaussian_filter(image0)
image0 = cv.bilateralFilter(image0, 50, 150, 50, borderType=cv.BORDER_DEFAULT)


image1 = cv.imread(tamper, 0)
image1 = gaussian_filter(image1)
image1 = cv.bilateralFilter(image1, 50, 150, 50, borderType=cv.BORDER_DEFAULT)


result = subtract(image0, image1)

# 将像素值低于30的部分置为0
point = 10
result[result < point] = 0
result[result >= point] = 255

cv.imwrite("FREE/substract_Gaussian.jpg", result)