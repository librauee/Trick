# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 12:51:21 2019

@author: Lee
"""

import tesserocr
from PIL import Image
from io import BytesIO
import time
from selenium import webdriver


class Auto(object):
    
    def __init__(self,username,password):
        self.browser=webdriver.Chrome()
        self.browser.get('http://my.hfut.edu.cn/login.portal')
        self.username=username
        self.password=password
        
    def check_login(self):
        try:
            text=self.browser.find_element_by_xpath('//a[@title="实验室准入"]')
            print("您已经成功登录！")
            return True
        except:
            print("验证码错误！")
            return False
            
    
    def get_screenshot(self):
        
        screenshot=self.browser.get_screenshot_as_png()
        return Image.open(BytesIO(screenshot))
    
    def get_geetest_image(self):

#    a=browser.find_element_by_id('captchaImg')
#    location=a.location 
#    
#    size=a.size
#    print(location['x'])
#    
#    bottom,top,left,right=location['y'],location['y']+size['height'],location['x'],location['x']+size['width']
#    print("验证图片位置",bottom,top,left,right)
        bottom,top,left,right=287,307,920,974
        screenshot=self.get_screenshot().convert('RGB')
        captcha_img=screenshot.crop((left,bottom,right,top))
        captcha_img.save('captcha.jpg')
        
    def ocr():

        image=Image.open('captcha.jpg')
        image=image.convert('L')
        threshold=127
        table=[]
        for i in range(256):
            if i<threshold:
                table.append(0)
            else:
                table.append(1) 
        image=image.point(table,'1')
        result=tesserocr.image_to_text(image)
        print(result)
        return result
    
    
    
    def login(self):
    
        user_name=self.browser.find_element_by_id('username')
        pwd=self.browser.find_element_by_id('password')
        login_btn=self.browser.find_element_by_name('btn')   #登录按钮
        cap=self.browser.find_element_by_name('captcha')
        self.get_geetest_image()
        user_name.send_keys(self.username)              #输入用户名
        pwd.send_keys(self.password)                    #输入密码

        # result=ocr()
        result=input("请输入验证码：")
        cap.send_keys(result)
        
        login_btn=self.browser.find_element_by_name('btn')#登陆按钮
        login_btn.send_keys("\n")       #点击登陆按钮
        time.sleep(2)
        flag=self.check_login()
        
        while not flag:
            self.login()
            
        

        
        
#    windows=browser.window_handles
#    browser.switch_to.window(windows[-1])
#    current=browser.current_window_handle#当前页面的句柄
#    browser.switch_to.window(current)
        
        
    def enter_article(self):
        
        js="""
        var elems = document.getElementsByClassName('patchContainer');
        for (var i=0;i<elems.length;i+=1){
         elems[i].style.display = 'block';
        }
        """
        # 调用js脚本
        self.browser.execute_script(js)

        time.sleep(2)
        lab=self.browser.find_element_by_xpath('//a[@title="实验室准入"]')

        lab.send_keys("\n")
        time.sleep(2)
        windows=self.browser.window_handles
        self.browser.switch_to.window(windows[-1])
        safe=self.browser.find_element_by_xpath('//a[@title="安全知识学习"]')
        safe.send_keys("\n")
        time.sleep(2)
        windows=self.browser.window_handles
        self.browser.switch_to.window(windows[-1])
        article=self.browser.find_element_by_xpath('//a[@class="zxxxy-summary"]')
        article.send_keys("\n")
        print("现在开始进行阅读……")
 
    
    def answer_confirm(self):
        # 每隔5分钟弹出确认窗口
        count=1
        while 1:
            try:
                confirm=self.browser.switch_to_alert()
                print(confirm.text)
                confirm.accept()
                print("您已经完成时长为{}分钟的阅读！".format(count*5))
                count+=1
                time.sleep(300)
            except:
                time.sleep(2)
                
                
                
                
if __name__=='__main__':
    
    username=input("请输入您的用户名：")
    password=input("请输入您的密码：")
    auto=Auto(username,password)
    auto.login()
    auto.enter_article()
    time.sleep(300)
    auto.answer_confirm()