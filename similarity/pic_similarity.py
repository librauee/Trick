# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 13:27:42 2019

@author: Lee
"""


import glob
import os
import sys
from functools import reduce

from PIL import Image

# EXTS = 'jpg', 'jpeg', 'JPG', 'JPEG', 'gif', 'GIF', 'png', 'PNG'
EXTS = 'jpg', 'jpeg', 'gif', 'png'


# 通过计算哈希值来得到该张图片的“指纹”
def avhash(im):
    # 判断参数im，是不是Image类的一个参数
    try:
        if not isinstance(im, Image.Image):
            im = Image.open(im)
    except Exception as e:
        print(e)
        return "ng"
    # resize，格式转换，把图片压缩成8*8大小，ANTIALIAS是抗锯齿效果开启，“L”是将其转化为
    # 64级灰度，即一共有64种颜色
    im = im.resize((8, 8), Image.ANTIALIAS).convert('L')
    # 递归取值，这里是计算所有
    # 64个像素的灰度平均值
    
    avg = reduce(lambda x, y: x + y, im.getdata()) / 64.

    print(bin(reduce(func_reduce_param, enumerate(map(lambda i: 0 if i < avg else 1, im.getdata())), 0)))
    # 比较像素的灰度，将每个像素的灰度与平均值进行比较，>=avg：1；<avg：0
    return reduce(func_reduce_param,
                  enumerate(map(lambda i: 0 if i < avg else 1, im.getdata())), 0)


def func_reduce_param(x, a):
    if type(a) == tuple:
        y = a[0]
        z = a[1]
    return x | (z << y)


# 比较指纹，等同于计算“汉明距离”（两个字符串对应位置的字符不同的个数）
def hamming(h1, h2):
    if h1 == "ng" or h2 == "ng":
        return "获取指纹失败。"
    h, d = 0, h1 ^ h2
    while d:
        h += 1
        d &= d - 1
    return h


def compare(img1, img2):
    if os.path.isfile(img1):
        print("源图为：{}".format(img1))
    else:
        print("给定的源图片：{} 不存在".format(img1))
        return "img1"

    if os.path.isfile(img2):
        print("对比图为：{}".format(img2))
    else:
        print("给定的对比图片：{} 不存在".format(img2))
        return "img2"

    ham = hamming(avhash(img2), avhash(img1))
    if type(ham) == int:
        if ham == 0:
            print("源图：{} 与对比图：{} 一样。{}".format(img1, img2, ham))
        elif ham <= 3:
            print("源图：{} 与对比图：{} 存在差异。{}".format(img1, img2, ham))
        elif ham <= 5:
            print("源图：{} 与对比图：{} 对比明显存在差异。{}".format(img1, img2, ham))
        elif ham <= 8:
            print("源图：{} 与对比图：{} 还能看到一点儿相似的希望。{}".format(img1, img2, ham))
        elif ham <= 10:
            print("源图：{} 与对比图：{} 这两张图片有相同点，但少的可怜啊。{}".format(img1, img2, ham))
        elif ham > 10:
            print("源图：{} 与对比图：{} 不一样。{}".format(img1, img2, ham))
    else:
        print("未知的结果，无法完成对比。")
    return ""


def compare_many_pic(img, abs_dir):
    if os.path.isfile(img):
        print("源图为：{}".format(img))
    else:
        print("给定的源图片：{} 不存在".format(img))
        print("Usage: image.jpg [dir]")
        return "img"
    if os.path.isdir(abs_dir):
        print("给定目录为：{}".format(abs_dir))
    else:
        print("给定的目录：{} 不存在".format(abs_dir))
        print("Usage: image.jpg [dir]")
        return "dir"

    h = avhash(img)

    os.chdir(abs_dir)
    images = []
    for ext in EXTS:
        images.extend(glob.glob('*.%s' % ext))
    print(images)

    seq = []
    prog = int(len(images) > 50 and sys.stdout.isatty())
    for f in images:
        seq.append((f, hamming(avhash(f), h)))
        if prog:
            perc = 100. * prog / len(images)
            x = int(2 * perc / 5)
            print('\rCalculating... [' + '#' * x + ' ' * (40 - x) + ']')
            print('%.2f%%' % perc, '(%d/%d)' % (prog, len(images)))
            sys.stdout.flush()
            prog += 1

    if prog: print("")
    for f, ham in sorted(seq, key=lambda i: i[1]):
        print("{}\t{}".format(ham, f))
    return ""


if __name__ == '__main__':

    compare(img1="./images/1.png", img2="./images/10.png")
    compare_many_pic(img="./images/1.png",abs_dir='./images')
