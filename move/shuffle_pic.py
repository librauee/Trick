# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 09:46:08 2019

@author: Lee
"""

import random
import os
import shutil

origin_list=list(range(1,10001))

random.shuffle(origin_list)

def move(src,dst,i):
    if not os.path.isdir(dst):
        os.makedirs(dst)
    s=src+'\\{}.pgm'.format(i)
    d=dst+'\\{}.pgm'.format(10000+i)
    shutil.copy(s,d)

src='F:\\1.01'
dst='F:\\train\cover'

#print(origin_list)
for i in origin_list[:4000]:
    dst='F:\\train\cover'
    move(src,dst,i)

for i in origin_list[4000:5000]:
    dst='F:\\valid\cover'
    move(src,dst,i)
    

for i in origin_list[5000:10000]:
    dst='F:\\test\cover'
    move(src,dst,i)



