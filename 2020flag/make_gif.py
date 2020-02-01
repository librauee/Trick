# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 22:45:32 2020

@author: Administrator
"""


import cv2
import os
import imageio
from itertools import cycle
 

def pic_cycle():
    path="pic"
    filenames=os.listdir(path)
    img_iter=cycle([cv2.imread(os.sep.join([path, x])) for x in filenames])
    while 1:
        cv2.imshow('2020Flag', next(img_iter))
        cv2.waitKey(500) 
        


def make_gif():
    gif_images=[]
    img_paths=os.listdir('pic')
    img_paths=[os.sep.join(['pic',i]) for i in img_paths]
    for path in img_paths:
        gif_images.append(imageio.imread(path))
    imageio.mimsave("a.gif",gif_images,fps=2)
        


if __name__=='__main__':
    
    make_gif()
    pic_cycle()
        
        