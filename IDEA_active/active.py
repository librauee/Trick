# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 15:16:45 2020

@author: Administrator
"""

import requests
import tkinter
import pyperclip
import zipfile
import os

def get_text(i):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    url = 'http://idea.medeming.com/jets/images/jihuoma.zip'
    r = requests.get(url, headers=headers)
    with open("active.zip", "wb") as f:
        f.write(r.content)
    zip_file = zipfile.ZipFile("active.zip")
    zip_list = zip_file.namelist()
    for f in zip_list:
        zip_file.extract(f, 'active')
    zip_file.close()
    with open(os.path.join('active', zip_list[i]), 'r')as f:
        text=f.read()
    return text


def show_text(i):
    global active_code
    text=tkinter.Text(win,width=55,height=18)
    text.place(x=20,y=20)
    active_code=get_text(i)
    text.insert(tkinter.INSERT,str(active_code))


def send_to_clibboard():
    pyperclip.copy(active_code)


win=tkinter.Tk()
win.title("JetBrains​全家桶激活码提取器 @老肥码码码 V2.0")
win.geometry("450x350")
label=tkinter.Label(win,text="老版本")
label.place(x=60,y=270)
label=tkinter.Label(win,text="新版本(2018后)")
label.place(x=200,y=270)
button=tkinter.Button(win,text="获取激活码1",command=lambda :show_text(0))
button.place(x=60,y=300)
button=tkinter.Button(win,text="获取激活码2",command=lambda :show_text(1))
button.place(x=200,y=300)
button=tkinter.Button(win,text="复制激活码",command=send_to_clibboard)
button.place(x=340,y=300)
win.mainloop()





