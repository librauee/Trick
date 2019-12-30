# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 14:42:44 2019

@author: Lee
"""

from pymongo import MongoClient
import pandas as pd



"""
数据预处理
"""
db=MongoClient().github
data=pd.DataFrame(list(db['day'].find()))
data=data.drop(columns='_id',axis=0)
data['count']=data['count'].apply(pd.to_numeric)

"""
提交次数的频数统计
"""
day_count=data.groupby('count').count()['day']
count=list(day_count.index)
day=list(day_count.values)
print(day)
print(count)

"""
提交代码最多的一天
"""

print(data.sort_values(by="count",ascending=False))



# 数据预处理

data1=pd.DataFrame(list(db['repo'].find()))
data1=data1.drop(columns='_id',axis=0)
data1['count']=data1['count'].apply(pd.to_numeric)


# 提交次数的频数统计

month_count=data1.groupby('month').count()
print(month_count)
month_repo=data1.groupby(by=['month']).sum()
print(month_repo)
month=list(month_repo.index)
count=list(month_repo['count'].values)

print(sum(count))

