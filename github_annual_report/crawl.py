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
import time
import random



class Github(object):
    
    def __init__(self):
        """
        初始化
        """
        self.user_agent=[
             "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
             "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
             "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
             "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
             "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
             "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
             "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
             "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
             "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
             "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
             "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
             "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
             "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
             "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
             "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)"
             ]
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


            
    def get_repo_id(self):
        """
        获取所有仓库以及对应id
        """
        repo=dict()
        r=requests.get(url=self.url+'?tab=repositories',headers=self.headers)
        tree=etree.HTML(r.text)
        links=tree.xpath('//div[@class="d-inline-block mb-1"]/h3/a/@href')
        print(links)
        links=['https://github.com'+i for i in links]
        for link in links:
            headers={'User-Agent': random.choice(self.user_agent)}
            r=requests.get(url=link,headers=headers)
            tree=etree.HTML(r.text)

            try:
                repo_id=tree.xpath('//div[@class="flex-auto f6 mr-3"]/a[2]/@href')[0]
                repo[repo_id[10:-48]]=repo_id[-40:]
                time.sleep(5)
            except Exception as e:
                print(e)
                time.sleep(5)

        return repo
 

        
    def get_commit(self):
        """
        按仓库爬取代码提交情况
        """   
        repo=self.get_repo_id()
        #repo={'Emojis': 'fe3b56bc1ebada24502030257fb92c2a46a12969', 'BlockChain': '9f26f0568f9a72472a394577495fead08dc5e631', 'Trick': 'c768bac1ef25553034b8259b0432747ec7b93e2b', 'Algorithm': '60646324bb62c46dd8f48fb89fbf8ba01fe0c92b', 'Reptile': '5f063ea9dffaae8a8ab854ac9b51c3f5b5d6ce53', 'SE': '6b55f6326a52199993f808c38c1d12b0e1d08bc5', 'leetcode': '45c12c9cbaf2d0d87e2543b49f4b0cbf9096b3bf', 'Steganalysis': 'f7844698bff217ff206b9a3de15ccec708951c83', 'DeepLearning': 'b8080938a4b22395379be9032266df36cb5491e6', 'YYSLink': '56a6b65280e50c207c0700b0359e509a75972be8', 'Statistical-Learning': 'c988aea60ba0ed5a01b10d31f4a823eb3c75f3b7','DataMining': '302e161d441a5831271a0bb05c115a81f335e527'}
        
        for key,value in repo.items():
            commit=[]   
            contents=[]
            url='https://github.com/librauee/{}/commits/master'.format(key)
            r=requests.get(url,headers=self.headers)
 
            tree=etree.HTML(r.text)
            commit_time=tree.xpath('//relative-time[@class="no-wrap"]/@datetime')
            older=tree.xpath('//button[@class="btn btn-outline BtnGroup-item"]/text()')
            content=tree.xpath('//p[@class="commit-title h5 mb-1 text-gray-dark "]/a/text()')
            commit.extend(commit_time)
            contents.extend(content)
            if len(older)!=2:
            
                i=0
                while 1:                
                    params={
                            'after': '{} {}'.format(value,35*i-1),
                            '_pjax': '#js-repo-pjax-container'
                            }   
                    url='https://github.com/librauee/{}/commits/master'.format(key)
                    r=requests.get(url,headers=self.headers,params=params)
                    tree=etree.HTML(r.text)
                    commit_time=tree.xpath('//relative-time[@class="no-wrap"]/@datetime')
                    older=tree.xpath('//button[@class="btn btn-outline BtnGroup-item"]/text()')
                    content=tree.xpath('//p[@class="commit-title h5 mb-1 text-gray-dark "]/a/text()')
                    commit.extend(commit_time)
                    contents.extend(content)
                    if len(older)!=0 and older[0]=='Older':
                        break                  
                    i+=1
            for i in range(len(commit)):
                item={
                        'repo':key,
                        'commit_time':commit[i],
                        'cotent':contents[i]
                        }
                self.db['time'].insert_one(item)

if __name__=='__main__':
    
    git=Github()
    git.get_month()
    git.get_day()
    git.get_commit()

