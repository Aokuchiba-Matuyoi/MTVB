import cv2 as cv

tool = cv.imread('IMG/5.6.jpg', 0)

def Gaussian(tool):
    Gaussian_Blur = [[0.095, 0.118, 0.095], [0.118, 0.148, 0.118], [0.095, 0.118, 0.095]]
    test_tool = tool
    for i in range(1, tool.shape[0] - 1):
        for j in range(1, tool.shape[1] - 1):
            # print(tool[i - 1:i + 2, j - 1:j + 2])
            tiny_tool = tool[i - 1:i + 2, j - 1:j + 2]
            tiny_sum = 0
            for l in range(3):
                for m in range(3):
                    tiny_sum = tiny_tool[l][m] * Gaussian_Blur[l][m] + tiny_sum
            # print(tiny_average)
            test_tool[i][j] = tiny_sum
    print(test_tool)
    return test_tool


x = Gaussian(tool)
cv.imwrite('TEST/0.3.jpg', x)
