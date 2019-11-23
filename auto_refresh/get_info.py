# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 23:19:26 2019

@author: Administrator
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from lxml import etree
from apscheduler.schedulers.blocking import BlockingScheduler
import time


def sendemail(title):
    
    
    message=MIMEMultipart()
    att1=MIMEText(open('{}.xlsx'.format(title),'rb').read(),'base64','utf-8')
    att1['Content-Type']='application/octet-stream'
    att1['Content-Disposition']='attatchment;filename='+title
    message.attach(att1)
    
    msg_from='870407139@qq.com'                                 #发送方邮箱
    passwd=''                                   #填入发送方邮箱的授权码
    receivers=['870407139@qq.com']                              #收件人邮箱
                            
    subject="".format(title)                                    #主题     

    message['Subject'] = subject
    message['From'] = msg_from
    message['To'] = ','.join(receivers)
    
    try:
        s=smtplib.SMTP_SSL("smtp.qq.com",465)                   #邮件服务器及端口号
        s.login(msg_from, passwd)
        s.sendmail(msg_from, message['To'].split(','), message.as_string())
        print("发送成功")
    except Exception as e:
        print(e)
        print("发送失败")
    finally:
        s.quit()
        


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
        sendemail(title)
    else:
        print("暂无考试安排~")


if __name__=='__main__':

    print("开启定时任务……")
    
    
    scheduler=BlockingScheduler()
    scheduler.add_job(func=get_news,trigger='interval',minutes=10,misfire_grace_time=10)
    scheduler.start()