#!/usr/bin/env python3
import cv2
import numpy as np
import matplotlib.pyplot as pltimport
import time

img=cv2.imread('111/1563325813.png')
# img=img[14:-15,13:-14]
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
print("num of contours: {}".format(len(contours)))


rect = cv2.minAreaRect(contours[1])  #获取蓝色矩形的中心点、宽高、角度


'''
retc=((202.82777404785156, 94.020751953125),
 (38.13406753540039, 276.02105712890625),
 -75.0685806274414)
'''

width = int(rect[1][0])
height = int(rect[1][1])
angle = rect[2]
print(angle)

if width < height:  #计算角度，为后续做准备
  angle = angle - 90
print(angle)

# if  angle < -45:
#     angle += 90.0
#        #保证旋转为水平
# width,height = height,width
src_pts = cv2.boxPoints(rect)

# box = cv2.boxPoints(rect)
# box = np.int0(box)
# cv2.drawContours(img_box, [box], 0, (0,255,0), 2)
#

dst_pts = np.array([[0, height],
                    [0, 0],
                    [width, 0],
                    [width, height]], dtype="float32")
M = cv2.getPerspectiveTransform(src_pts, dst_pts)
warped = cv2.warpPerspective(img, M, (width, height))

if angle<=-90:  #对-90度以上图片的竖直结果转正
    warped = cv2.transpose(warped)
    warped = cv2.flip(warped, 0)  # 逆时针转90度，如果想顺时针，则0改为1
    # warped=warped.transpose
cv2.imshow('wr1',warped)
cv2.waitKey(0)


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    pass
