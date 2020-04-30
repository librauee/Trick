import hashlib
import random
import requests
import tkinter
import pyperclip


def translate(q,lan_from,lan_to):
    '''
    调用百度翻译API
    '''
    appid = entry1.get()
    key = entry2.get()
    url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
    salt = random.randint(1, 65536)
    sign = hashlib.md5((str(appid)+str(q)+str(salt)+str(key)).encode('utf-8')).hexdigest()
    params = {
        'from' :lan_from,
        'to' :lan_to,
        'salt' : salt,
        'sign' : sign,
        'appid' : appid,
        'q': q
    }
    r = requests.get(url,params=params)
    txt = r.json()
    if txt.get('trans_result', -1) == -1:
        print('ERROR Code：{}'.format(txt))
        return q
    return txt['trans_result'][0]['dst']

def get_content(q):

    en=translate(q,'zh','en')
    kor=translate(en,'en','kor')
    zh=translate(kor,'kor','zh')
    print(zh)
    return zh

def show_text():
    global content
    word=entry3.get()
    print(word)
    content=get_content(word)
    text.insert(tkinter.INSERT,str(content))

def send_to_clibboard():
    pyperclip.copy(content)

def delete():
    entry3.delete(0, 'end')
    text.delete('1.0', 'end')


win=tkinter.Tk()
win.title("论文降重助手 @老肥码码码 V1.0")
win.geometry("400x400")
content1=tkinter.Variable()
entry1 = tkinter.Entry(win, text=content1, width=20,highlightcolor='red', highlightthickness=1)
entry1.place(x=65, y=5)
content2=tkinter.Variable()
entry2 = tkinter.Entry(win, text=content2, width=20,highlightcolor='red', highlightthickness=1,show='*')
entry2.place(x=240, y=5)
word=tkinter.Variable()
entry3 = tkinter.Entry(win, text=word, width=50,highlightcolor='red', highlightthickness=1)
entry3.place(x=20, y=60)
tkinter.Label(win, text='请输入您需要降重的文本内容：').place(x=20, y=35)
tkinter.Label(win, text='appid:').place(x=20, y=5)
tkinter.Label(win, text='key:').place(x=210, y=5)
tkinter.Label(win, text='文本处理结果').place(x=20, y=130)

button1=tkinter.Button(win,text="开始",command=show_text,width=10)
button1.place(x=20,y=90)
button2=tkinter.Button(win,text="清除",command=delete,width=10)
button2.place(x=160,y=90)
button3=tkinter.Button(win,text="复制",command=send_to_clibboard,width=10)
button3.place(x=300,y=90)

text = tkinter.Text(win, width=50, height=15)
text.place(x=20, y=160)

win.mainloop()









