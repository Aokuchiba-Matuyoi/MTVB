import cv2 as cv


if __name__ == '__main__':
    image = cv.imread('FREE/test.jpg', 0)
    img_bilateral = cv.bilateralFilter(image, 99, 150, 50, borderType=cv.BORDER_DEFAULT)
    cv.imwrite('FREE/test.jpg', img_bilateral)

