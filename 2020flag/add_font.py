# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 23:25:58 2020

@author: Administrator
"""

from PIL import Image,ImageDraw,ImageFont



def add_font(text,i):

    font=ImageFont.truetype('simhei.ttf', 80)
    img=Image.open('a.jpg')
    draw=ImageDraw.Draw(img)
    draw.text((110,110),text,(0,0,0),font=font)
    #img.show()
    img.save('pic/{}.png'.format(i))
    
    
if __name__=='__main__':
    text=['2020Flag','发CCFSCI','平安喜乐','坚持锻炼','发量不变','更爱肥肥']
    for i in range(len(text)):
        add_font(text[i],i)