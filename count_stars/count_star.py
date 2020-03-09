# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 21:53:24 2020

@author: 老肥
@WeChat Official Accounts:老肥码码码
@Wechat: jennnny1216

Happy Python，Happy Life!
"""

import requests
from prettytable import PrettyTable

def crawl(name):
    '''
    爬取某个id的所有仓库信息，并做简单统计
    '''
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    flag=True
    repo=[]
    page=1
    while flag:        
        url='https://api.github.com/users/{}/repos?page={}'.format(name,page)
        try:
            r=requests.get(url,headers=headers)
            data=r.json()
            if len(data) == 0:
                flag=False
            for i in data:
                if not i['fork']:
                    repo.append([i['name'],i['language'],i['stargazers_count'],i['forks_count']])
            page+=1
        except Exception as e:
            print(e) 
            break
    repo=sorted(repo, key=lambda x: x[2], reverse=True)
    repo.append(['Total','/',sum([i[2] for i in repo]), sum([i[3] for i in repo])])
    return repo


def pretty_print(repo):
    '''
    以表格形式美观地打印输出
    '''    
    x=PrettyTable()
    x.field_names=["Repository","language","Star","Fork"]
    for i in repo:
        x.add_row(i)
    print(x)
    
    
if __name__=='__main__':
    print("欢迎使用GitHub仓库统计查询工具（By老肥）")
    name=input("请输入你的GitHub用户名：")
    print("Waiting……")
    repo=crawl(name)
    pretty_print(repo)
    