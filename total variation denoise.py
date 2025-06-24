import cv2 as cv
import numpy as np


def tv(img, iter):
    ep = 1
    nx = img.shape[0]
    ny = img.shape[1]
    dt: float = 0.25
    lam = 0
    ep2 = ep * ep
    image: float = np.zeros((nx, ny))
    image0:float = np.zeros((nx, ny))

    for i in range(nx):
        for j in range(ny):
            image0[i][j]: float = img[i][j]
            image[i][j]: float = img[i][j]

    for t in range(iter):
        t = str(t+1)
        print("迭代第"+t+"遍")
        for i in range(nx):
            for j in range(ny):
                if (i + 1) < nx:
                    tmp_i1: int = i + 1
                else:
                    tmp_i1: int = nx - 1
                if (j + 1) < ny:
                    tmp_j1: int = j + 1
                else:
                    tmp_j1: int = ny - 1
                if (i - 1) > -1:
                    tmp_i2: int = i - 1
                else:
                    tmp_i2: int = 0
                if (j - 1) > -1:
                    tmp_j2: int = j - 1
                else:
                    tmp_j2: int = 0

                tmp_x: float = 0
                tmp_x = (image[i][tmp_j1] - image[i][tmp_j2]) / 2
                tmp_y: float = 0
                tmp_y = (image[tmp_i1][j] - image[tmp_i2][j]) / 2
                tmp_xx: float = 0
                tmp_xx = image[i][tmp_j1] + image[i][tmp_j2] - image[i][j] * 2
                tmp_yy: float = 0
                tmp_yy = image[tmp_i1][j] + image[tmp_i2][j] - image[i][j] * 2
                tmp_dp: float = 0
                tmp_dp = image[tmp_i1][tmp_j1] + image[tmp_i2][tmp_j2]
                tmp_dm: float = 0
                tmp_dm = image[tmp_i2][tmp_j1] + image[tmp_i1][tmp_j2]
                tmp_xy: float = 0
                tmp_xy = (tmp_dp - tmp_dm) / 4
                tmp_num: float = 0
                tmp_num = tmp_xx * (tmp_y * tmp_y + ep2) - 2 * tmp_x * tmp_y * tmp_xy + tmp_yy * (tmp_x * tmp_x + ep2)
                tmp_den: float = 0
                tmp_den = pow((tmp_x * tmp_x + tmp_y * tmp_y + ep2), 1.5)
                image[i][j] += dt * (tmp_num / tmp_den + lam * (image0[i][j] - image[i][j]))

    print("迭代完成")
    new_img = np.copy(img)
    for i in range(nx):
        for j in range(ny):
            tmp: int = image[i][j]
            tmp = max(0, min(tmp, 255))
            new_img[i][j] = tmp
    return new_img


test_01 = cv.imread("result/4.4.jpg", 0)
result = tv(test_01, 10)
cv.imwrite("result/2.jpg", result)
