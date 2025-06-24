import cv2 as cv
import numpy as np


def words_scan(num):
    img = cv.imread('result\\' + str(num) + ".jpg", 0)

    ret, img = cv.threshold(img,25, 255, cv.THRESH_BINARY_INV)
    cv.imshow('img', img)
    cv.waitKey(0)
    cv.destroyAllWindows()


    # 膨胀、腐蚀
    element1 = cv.getStructuringElement(cv.MORPH_RECT, (30, 9))
    element2 = cv.getStructuringElement(cv.MORPH_RECT, (24, 6))

    # 膨胀一次，让轮廓突出
    dilation = cv.dilate(img, element2, iterations=1)
    cv.imshow('img', dilation)
    cv.waitKey(0)
    cv.destroyAllWindows()

    # 腐蚀一次，去掉细节
    erosion = cv.erode(dilation, element1, iterations=1)
    cv.imshow('img', erosion)
    cv.waitKey(0)
    cv.destroyAllWindows()

    # 再次膨胀，让轮廓明显一些
    dilation2 = cv.dilate(erosion, element2, iterations=2)
    cv.imshow('img', dilation2)
    cv.waitKey(0)
    cv.destroyAllWindows()

    #  查找轮廓和筛选文字区域
    region = []
    contours, hierarchy = cv.findContours(dilation2, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    for i in range(len(contours)):
        cnt = contours[i]

        # 计算轮廓面积，并筛选掉面积小的
        area = cv.contourArea(cnt)
        if area > 100000 or area<10000: continue

        # 找到最小的矩形
        rect = cv.minAreaRect(cnt)
        print ("rect is: ")
        print (rect)

        # box是四个点的坐标
        box = cv.boxPoints(rect)
        box = np.int0(box)

        # 计算高和宽
        height = abs(box[0][1] - box[2][1])
        width = abs(box[0][0] - box[2][0])

        # 根据文字特征，筛选那些太细的矩形，留下扁的
        if (height > width * 1.3):
            continue

        region.append(box)

    # 设置一张全白图，以加上轮廓测试效果
    img_test = np.ones((img.shape[0], img.shape[1]), np.uint8)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img_test[i][j] == 1:
                img_test[i][j] = 255


    # 绘制轮廓
    for box in region:
        cv.drawContours(img_test, [box], 0, (0, 255, 0), 2)

    cv.imshow('img', img_test)
    cv.waitKey(0)
    cv.destroyAllWindows()



    # cv.imwrite('word_sacn/1.jpg', img_result)


words_scan(0.31)
