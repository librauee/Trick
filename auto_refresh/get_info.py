# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 19:16:00 2019

@author: Lee
"""

import requests
from lxml import etree
from apscheduler.schedulers.blocking import BlockingScheduler
import time



url='http://pyb.hfut.edu.cn/tzgg/list1.htm'
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}

def get_news():
    now=time.time()
    now=time.localtime(now)
    now=time.strftime("%Y-%m-%d %H:%M:%S",now)
    print(now)
    r=requests.get(url,headers=headers)
    r.encoding=r.apparent_encoding
    tree=etree.HTML(r.text)
    title=tree.xpath('//tr/td/a/@title')[0]
    href=tree.xpath('//tr/td/a/@href')[0]
    if '考试安排' in title:
        print(title)
        r2=requests.get('http://pyb.hfut.edu.cn/'+href,headers=headers)
        with open('{}.xlsx'.format(title),'wb') as f:
            f.write(r2.content)
        print('{}.xlsx 已经成功下载！'.format(title))
    else:
        print("暂无考试安排~")

        
        
        
if __name__=='__main__':

    print("开启定时任务……")
    scheduler=BlockingScheduler()
    scheduler.add_job(func=get_news,trigger='interval',minutes=30,misfire_grace_time=10)
    scheduler.start()
