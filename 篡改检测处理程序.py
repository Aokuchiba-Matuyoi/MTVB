import os

from PIL import Image
import cv2 as cv
import numpy as np
import tf as tf


# image = cv.imread('IMG/2.1.jpg')
# imgaex = cv.imread('IMG/2.1.jpg')
# image_result = (image | imgaex)
# print(image_result)
for filename in os.listdir("IMG"):
    filenamey = filename.split('.')[0]
    print('前缀为：'+filenamey)
    filenamex = filename.split('.')[1]
    print('后缀为：' + filenamex)

    # print(image)

    image_origin = cv.imread('IMG/{filenamey}.1.jpg' \
                                 .format(filenamey=filenamey), 0)
    # if int(filenamex) == 1:
    #     cv.imwrite('IMG_x/%s' % (filenamey) + '.' + '%s.jpg' % (filenamex), image_origin)
    if image_origin is not None:
        if int(filenamex) != 1:
            image_modify = cv.imread('IMG/%s'%(filenamey)+'.'+'%s.jpg'%(filenamex), 0)
            if image_modify is not None:
                if image_modify.shape != image_origin.shape:
                    continue
                else:
                    image_result = (image_modify - image_origin)
                    print('已成功处理图片' + filenamey + '.' + filenamex + '.jpg')
                # for x in image_result:
                #     for y in x:
                #         for z in y:
                #             i  f int(z) == 0:
                #                 z = int(255)
                #             elif int(z) != 0:
                #                 z = int(0)                    该列表为只读列表，不能通过遍历修改
                ret, image_result = cv.threshold(image_result, 0, 255, cv.THRESH_BINARY_INV)
                # print(image_result)
                cv.imwrite('IMG_x/%s'%(filenamey)+'.'+'%s.jpg'%(filenamex), image_result)
            else:
                print('无法读取图片')
        print('已成功保存图片'+filenamey+'.'+filenamex+'.jpg')
    else:
        print('无法读取图片')
