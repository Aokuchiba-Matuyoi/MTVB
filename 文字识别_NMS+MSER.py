import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def non_max_suppression_fast(boxes, overlapThresh):
    """
    boxes: boxes为一个m*n的矩阵，m为bbox的个数，n的前4列为每个bbox的坐标，
           格式为（x1,y1,x2,y2），有时会有第5列，该列为每一类的置信
    overlapThresh: 最大允许重叠率
    """
    # if there are no boxes, return an empty list
    if len(boxes) == 0:
        return []

    # if the bounding boxes are integers, convert them to floats
    # this is important since we'll be doing a bunch of divisions
    if boxes.dtype.kind == "i":
        boxes = boxes.astype("float")

    # initialize the list of picked indexes
    pick = []

    # grab the coordinates of all bounding boxes respectively
    x1 = boxes[:,0]  # startX
    y1 = boxes[:,1]  # startY
    x2 = boxes[:,2]  # endX
    y2 = boxes[:,3]  # endY
    # probs = boxes[:,4]

    # compute the area of the bounding boxes and sort the bboxes
    # by the bottom y-coordinate of the bboxes by ascending order
    # and grab the indexes of the sorted coordinates of bboxes
    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    idxs = np.argsort(y2)

    # if probabilities are provided, sort by them instead
    # idxs = np.argsort(probs)

    # keep looping while some indexes still remain in the idxs list
    while len(idxs) > 0:
        # grab the last index in the idxs list (the bottom-right box)
        # and add the index value to the list of picked indexes
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)

        # find the largest coordinates for the start of the bbox
        # and the smallest coordinates for the end of the bbox
        # in the rest of bounding boxes.
        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])

        # the width and height of the bounding box
        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)
        # the ratio of overlap in the bounding box
        overlap = (w * h) / area[idxs[:last]]

        # delete all indexes from the index list that overlap is larger than overlapThresh
        idxs = np.delete(idxs, np.concatenate(([last], np.where(overlap > overlapThresh)[0])))

    # return only the bounding boxes that were picked using the
    # integer data type
    return boxes[pick].astype("int")

path = 'images_in_the_paper/man_3.jpg'
img = cv.imread(path)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)  # 灰度图
vis_1 = img.copy()
vis_2 = img.copy()

# get mser object
mser = cv.MSER_create(delta=5, min_area=10, max_variation=0.5)
# Detect MSER regions
regions, boxes = mser.detectRegions(gray)

# 绘制文本区域（不规则轮廓）
hulls = [cv.convexHull(p.reshape(-1, 1, 2)) for p in regions]
cv.polylines(img, hulls, 1, (0, 255, 0), 1)

# plt.imshow(img, cmap='gray')
# plt.show()

# 两种绘制矩形轮廓
# for box in boxes:
#     x, y, w, h = box
#     cv2.rectangle(vis_1, (x,y),(x+w, y+h), (255, 0, 0), 1)

keep = []
for hull in hulls:
    x, y, w, h = cv.boundingRect(hull)
    keep.append([x, y, x + w, y + h])
    cv.rectangle(vis_1, (x, y), (x + w, y + h), (255, 0, 0), 1)
print("%d bounding boxes before nms" % (len(keep)))

# plt.imshow(vis_1, cmap='gray')
# plt.show()
# cv.imwrite("MSER/mser.png", vis_1)

# 使用非极大值抑制获取不重复的矩形框
pick = non_max_suppression_fast(np.array(keep), overlapThresh=0.4)
print("%d bounding boxes after nms" % (len(pick)))

# loop over the picked bounding boxes and draw them
for (startX, startY, endX, endY) in pick:
    cv.rectangle(vis_2, (startX, startY), (endX, endY), (0, 0, 255), 1)
# plt.imshow(vis_2, cmap='gray')
# plt.show()
# cv.imwrite("images_in_the_paper/man_3.1.jpg", vis_2)

img_origin = cv.imread("images_in_the_paper/man_2.jpg")
img_origin = cv.cvtColor(img_origin, cv.COLOR_BGR2GRAY)

for (startX, startY, endX, endY) in pick:
    print(startX, endX, startY, endY)
    for i in range(startX, endX):
        print(i)
        for j in range(startY, endY):
            print(j)
            if vis_2[j][i][0] == 255:
                vis_2[j][i][0] = 0
            else:
                vis_2[j][i][0] = 255
            img_origin[j][i] = vis_2[j][i][0]

# plt.imshow(img_origin, cmap='gray')
# plt.show()
kernel = np.ones((3, 3), np.uint8)
for x in range(2):
    img_origin = cv.erode(img_origin, kernel, 1)
# cv.imwrite("images in the paper/man_3.5.jpg", img_origin)



# plt.imshow(vis_2, cmap='gray')
# plt.show()


# 合并图片
# boxing_list = [img, vis_1, vis_2]
# plt.imshow(vis_2, cmap='gray')
# boxing = np.concatenate(boxing_list, axis=0)
#
# plt.figure(figsize=(10, 20))  # w,h
# plt.imshow(boxing, cmap='gray')
# plt.show()


# 得到文字区域
img = vis_2
# plt.imshow(img, cmap='gray')
# plt.show()

text_mask = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)
for contour in hulls:
    cv.drawContours(text_mask, [contour], -1, (255, 255, 255), -1)



# plt.imshow(text_mask, cmap='gray')
# plt.show()


img = cv.imread(path)
img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# 两图相加
# text_region = text_mask + img

text_region = cv.bitwise_and(img, text_mask, mask=None)
ret, text_region = cv.threshold(text_region, 15, 255, cv.THRESH_BINARY_INV)

text_region = cv.bitwise_and(text_region, text_mask, mask=None)
plt.imshow(text_region, cmap='gray')
plt.show()


img_origin = cv.imread("images_in_the_paper/man_3.2.jpg")
plt.imshow(img_origin, cmap='gray')
plt.show()

img_origin = cv.cvtColor(img_origin, cv.COLOR_BGR2GRAY)
plt.imshow(img_origin, cmap='gray')
plt.show()



text_region = text_mask + img_origin

plt.imshow(text_region, cmap='gray')
plt.show()




# plt.imshow(text_region, cmap='gray')
# plt.show()

# 黑白反转
# ret, text_region = cv.threshold(text_region, 15, 255, cv.THRESH_BINARY_INV)
#
# plt.imshow(text_region, cmap='gray')
# plt.show()