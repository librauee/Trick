# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 09:55:30 2019

@author: Lee
"""
import os
import argparse
from PIL import Image


CELLSIZE = 128

'''图片读取'''
def readImage(img_path, target_size=(64, 64)):
	img = Image.open(img_path)
	img = img.resize(target_size)
	return img


'''图片生成器'''
def yieldImage(target_dir, idx, target_size):
	img_paths = sorted([os.path.join(target_dir, imgname) for imgname in os.listdir(target_dir)])
	idx = (idx + 1) % len(img_paths)
	return readImage(img_paths[idx], target_size), idx


'''解析模板'''
def parseTemplate(template_path):
	template = []
	with open(template_path, 'r') as f:
		for line in f.readlines():
			if line.startswith('#'):
				continue
			template.append(line.strip('\n').split(','))
	return template


'''主函数'''
def main(pictures_dir, template_path):
	template = parseTemplate(template_path)

	w = len(template[0])
	h = len(template)
	image_new = Image.new('RGBA', (CELLSIZE*w, CELLSIZE*h))
	img_idx = -1
	for y in range(h):
		for x in range(w):
			if template[y][x] == '1':
				img, img_idx = yieldImage(pictures_dir, img_idx, (CELLSIZE, CELLSIZE))
				image_new.paste(img, (x*CELLSIZE, y*CELLSIZE))
	image_new.show()
	image_new.save('picturewall520.png')


'''run'''
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Picture Wall Generator.")
	parser.add_argument('-t', dest='template_path', help='Template path.', default='templates/2.tmp')
	parser.add_argument('-p', dest='pictures_dir', help='Pictures dir.', default='parrot')
	args = parser.parse_args()
	template_path = args.template_path
	pictures_dir = args.pictures_dir
	main(pictures_dir, template_path)