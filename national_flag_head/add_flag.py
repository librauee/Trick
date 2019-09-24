# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 20:26:18 2019

@author: Lee
"""

import cv2
# 读取头像和国旗图案，提前文件夹下保存红旗照片，以flag命名，头像照片以head命名
img_head = cv2.imread('head.jpg')
img_flag = cv2.imread('flag.jpg')
# 获取头像和国旗图案宽度
w_head, h_head = img_head.shape[:2]
w_flag, h_flag = img_flag.shape[:2]
# 计算图案缩放比例
scale = w_head / w_flag / 8
# 缩放图案
img_flag = cv2.resize(img_flag, (0, 0), fx=scale, fy=scale)
# 获取缩放后新宽度
w_flag, h_flag = img_flag.shape[:2]
# 按3个通道合并图片
for c in range(0, 3):
    img_head[w_head - w_flag:, h_head - h_flag:, c] = img_flag[:, :, c]
# 保存最终结果
cv2.imwrite('new_head.jpg', img_head)