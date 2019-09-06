# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 20:06:31 2019

@author: Lee

图片批量重命名
"""



import os
 
class ImageRename():
     def __init__(self):
         self.path = 'D:/BaiduNetdiskDownload/肥肥'
 
     def rename(self):
         filelist = os.listdir(self.path)
         total_num = len(filelist) 
         i = 0
         for item in filelist:
             if item.endswith('.jpg'):
                 src = os.path.join(os.path.abspath(self.path), item)
                 dst = os.path.join(os.path.abspath(self.path),  str(i) + '.jpg')
                 os.rename(src, dst)
                 print('converting %s to %s ...' % (src, dst))
             i+=1
         print('total %d to rename & converted %d jpgs' % (total_num, i))
         
         
class ImageRename2():  
    def __init__(self):
         self.path = 'parrot'   
    
    def rename(self):
        for idx, each in enumerate(os.listdir(self.path)):
	        os.rename(os.path.join(self.path, each), os.path.join(self.path, '%s.jpg' % idx))
 
if __name__ == '__main__':
    newname = ImageRename2()
    newname.rename()