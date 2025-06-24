import cv2 as cv
import numpy as np

def median_filter(img, K_size=5):
    if len(img.shape) == 3:
        H, W, C = img.shape
    else:
        img = np.expand_dims(img, axis=-1)
        H, W, C = img.shape

    # Zero padding
    pad = K_size // 2
    out = np.zeros((H + pad * 2, W + pad * 2, C), dtype=float)
    out[pad: pad + H, pad: pad + W] = img.copy().astype(float)

    # Filtering
    tmp = out.copy()
    for y in range(H):
        for x in range(W):
            for c in range(C):
                out[pad + y, pad + x, c] = np.median(tmp[y: y + K_size, x: x + K_size, c])

    out = np.clip(out, 0, 255)
    out = out[pad: pad + H, pad: pad + W].astype(np.uint8)

    return out

# 读取灰度图像
x = cv.imread("IMG/2.2.jpg", 0)
x = median_filter(x, K_size=99)  # 应用中值滤波
cv.imwrite("FREE/2.2.jpg", x)