# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 12:56:18 2019

@author: Lee
"""

import requests
from lxml import etree
import re
from pymongo import MongoClient
import pandas as pd
import calendar
import datetime



class Github(object):
    
    def __init__(self):
        """
        初始化
        """
        
        self.headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
                      }
        self.url='https://github.com/librauee'
        self.regex=re.compile('[0-9]+')
        self.db=MongoClient().github
  
    def generate(self,startdate='2019-1-1',enddate='2020-1-1'):
        """
        生成每个月的第一天和最后一天
        """        
        date_range_list=[]
        startdate=datetime.datetime.strptime(startdate, '%Y-%m-%d')
        enddate=datetime.datetime.strptime(enddate, '%Y-%m-%d')
        while 1:
            next_month=startdate + datetime.timedelta(days=calendar.monthrange(startdate.year, startdate.month)[1])
            month_end=next_month - datetime.timedelta(days=1)
            if month_end<enddate:
                date_range_list.append((datetime.datetime.strftime(startdate,'%Y-%m-%d'),
                                        datetime.datetime.strftime(month_end,'%Y-%m-%d')))
                startdate = next_month
            else:
                return date_range_list

        
    def get_month(self):
        """
        按月爬取代码提交情况
        """        
        date=self.generate()
        for i in range(len(date)):
            date_from=date[i][0]
            date_to=date[i][1]
        
            params={
                'from': date_from,
                'to': date_to,
                'tab': 'overview',
                'include_header': 'no',
                'button': '',
                'utf8': '✓'
                }
            r=requests.get(url=self.url,headers=self.headers,params=params)
            tree=etree.HTML(r.text)
            repo=tree.xpath('//a[@data-hovercard-type="repository"]/text()')
            count=tree.xpath('//a[@class="f6 muted-link ml-lg-1 mt-1 mt-lg-0 d-block d-lg-inline "]/text()')
            repo=[i[9:] for i in repo]
            count=[self.regex.findall(i)[0] for i in count]
            for j in range(len(count)):
                item={
                    'month':i+1,
                    'repo':repo[j],
                    'count':count[j]
                    }
                self.db['month'].insert_one(item)
                
    def get_day(self):
        """
        按天爬取代码提交情况
        """          
        r=requests.get(url=self.url,headers=self.headers)
        count=re.findall('data-count="(.*?)" data-date',r.text)
        date=re.findall('data-date="(.*?)"/>',r.text)
        for i in range(len(count)):
            item={
              'day':date[i],
              'count':count[i]
                }
            self.db['day'].insert_one(item)
    
        

if __name__=='__main__':
    
    git=Github()
    git.get_month()
    git.get_day()
