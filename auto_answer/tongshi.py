# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 14:46:20 2019

@author: Lee
"""

import requests
from lxml import etree


class Answer(object):
    
    def __init__(self):
        
        self.url='http://syszr.hfut.edu.cn/redir.php'
        self.headers={
                'cookie': '',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
                }
        self.params={
                'catalog_id': 6,
                'cmd': 'dajuan_chakan',
                'huihuabh': 277801,
                'mode': 'test',
                }
        
    def get_html(self):
        
        r=requests.get(self.url,params=self.params,headers=self.headers)
        r.encoding=r.apparent_encoding
        return r.text
    
    def save_answer(self,text):
        
        tree=etree.HTML(text)
        _type=tree.xpath('//div[@class="shiti"]/span/text()')
        _type=[i[1:-1] for i in _type]
        question=tree.xpath('//div[@class="shiti"]/strong/text()|//div[@class="shiti"]/strong/p/text()[1]')
        question=[a.replace("\xa0","") for a in question]
        for i in range(len(_type)):
            if _type[i]=='单选题':
                loc=i
                break
        answer1=tree.xpath('//div[@class="shiti"]/text()[5]')[:loc]
        answer1=[a.replace("\r","").replace("\n","").replace(" ","")[9:] for a in answer1]
        answer2=tree.xpath('//div[@class="shiti"]/text()[6]')
        answer2=[a.replace("\r","").replace("\n","").replace(" ","")[9:] for a in answer2]
        with open('answer.txt','w') as f:
            for i in range(loc):
                f.write(question[i]+answer1[i]+"\n")
            for i in range(loc,len(_type)):
                f.write(question[i]+answer2[i-loc]+"\n")
        dic1=dict(zip(question[:loc],answer1[:loc]))

        dic2=dict(zip(question[loc:len(_type)],answer2))
        dic_tongshi=dic1.copy()
        dic_tongshi.update(dic2)
        print(dic_tongshi)
            
        

        
if __name__=='__main__':
    
    a=Answer()
    text=a.get_html()
    a.save_answer(text)

   