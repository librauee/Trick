# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 18:46:47 2020

@author: Administrator
"""


import requests
import cv2
import base64
import numpy as np 
import math

def get_mouth(dst_pic):
    
    
    with open(dst_pic, 'rb') as f:
        base64_data = base64.b64encode(f.read())
    url='https://api-cn.faceplusplus.com/facepp/v1/face/thousandlandmark'
    headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
    data={
          'api_key':'7dkZePi7VHwHoSNi3y-T31X3SPgVY2sI',
          'api_secret':'p7XMUe72zTGmdag_HT-UzVm7TRxxkXbA',
                            
          'return_landmark': 'mouth,nose',
          'image_base64': base64_data
                         }
    r=requests.post(url,headers=headers,data=data)
    mouth=r.json()['face']['landmark']['mouth']
    nose=r.json()['face']['landmark']['nose']
    print(nose)
    nose_y,nose_x=[],[]
    for k,v in nose.items():
        if 'nose_midline' in k:
            nose_y.append(v['y'])
            nose_x.append(v['x'])
#    point1=(nose_x[nose_y.index(max(nose_y))],max(nose_y))
#    point2=(nose_x[nose_y.index(min(nose_y))],min(nose_y))
#    k=(point1[1]-point2[1])/(point1[0]-point2[0])
#    print(point1)
#    print(point2)
#    angle=int(math.degrees(k)%360)
#    print(angle)            
    x,y=[],[]
    for i in mouth.values():

        y.append(i['y'])
        x.append(i['x'])
    y_max=max(y)
    y_min=min(y)
    x_max=max(x)
    x_min=min(x)
    middle_x=int((x_max+x_min)/2)
    middle_y=int((y_max+y_min)/2)
    size=(int(3*(x_max-x_min)),int(5*(y_max-y_min)))
    return (middle_x,middle_y),size

def add_mask(img_path,img_outPath):
    
    src_pic="mask.jpg"
    center,size=get_mouth(img_path)
    src=cv2.imread(src_pic)
    src=cv2.resize(src,size)
    dst=cv2.imread(img_path)
    # 掩膜
    mask=255*np.ones(src.shape, src.dtype)
#    new=cv2.imread('new.png')    
#    mask=cv2.resize(new,size)
    output=cv2.seamlessClone(src, dst, mask, center, cv2.NORMAL_CLONE)
    cv2.imwrite(img_outPath, output)


if __name__=='__main__':
    
    img_outPath="a.jpg"
    img_path="t.jpg"
    add_mask(img_path,img_outPath)
    
