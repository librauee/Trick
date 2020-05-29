import requests
import random
import pypinyin

class Poem_Crawl(object):

    def __init__(self):
        self.url='https://hanyu.baidu.com/hanyu/ajax/search_list'
        self.headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}

    def crawl(self,wd,flag):
        self.wd=wd
        poem_5=[]
        poem_7=[]
        try:
            params={
                'wd': self.wd,
                'from': 'poem',
                'pn': 1,
            }
            r=requests.get(self.url, headers=self.headers, params=params)
            ret_array=r.json()['ret_array']
            page=r.json()['extra']['total-page']
            for ret in ret_array:
                poem=ret['display_name'][0]
                if len(poem) == 7:
                    poem_7.append(poem)
                if len(poem) == 5:
                    poem_5.append(poem)

            for i in range(2,int(page)+1):
                params={
                    'wd': self.wd,
                    'from': 'poem',
                    'pn': i,
                }
                r=requests.get(self.url,headers=self.headers,params=params)
                ret_array=r.json()['ret_array']
                for ret in ret_array:
                    poem=ret['display_name'][0]
                    if len(poem)==7:
                        poem_7.append(poem)
                    if len(poem)==5:
                        poem_5.append(poem)

                # if len(poem_5)>100 and len(poem_7)>100:
                #     break

            if flag:
                return poem_7
            else:
                return poem_5
        except:
            return ["没有找到符合要求的诗句！"]

    def generate_poem(self,head_word,flag,head_or_tail):
        if head_or_tail==1:
            query='开头的诗句'
        else:
            query='结尾的诗句'
        heads=list(head_word)
        new_poem=[]
        for head in heads:
            poem_list=self.crawl(head+query,flag)
            poem=random.choice(poem_list)
            new_poem.append(poem)
        print("-----------------*********-----------------")
        print("\n".join(new_poem))
        print("-----------------*********-----------------")
        return new_poem

    def get_rhyme_set(self,poem):
        rhyme_list=[]
        for p in poem:
            last=pypinyin.lazy_pinyin(p[-1])[0]
            rhyme_list.append(last)
        return set(rhyme_list)


    def generate_rhyme(self,head_word,flag):
        rhyme_poem=[]
        heads=list(head_word)
        names=locals()
        count=1
        for head in head_word:
            names['poem_{}'.format(count)]=Poem.crawl(head+'开头的诗句',flag)
            names['rhyme_{}'.format(count)]=self.get_rhyme_set(names['poem_{}'.format(count)])
            count+=1
        for c in range(2,count):
            names['rhyme_{}'.format(c)]=names['rhyme_{}'.format(c)].intersection(names['rhyme_{}'.format(c-1)])
        if len(names['rhyme_{}'.format(count-1)])>0:
            for i in range(count-1):
                for j in names['poem_{}'.format(i+1)]:
                    if pypinyin.lazy_pinyin(j[-1])[0]==list(names['rhyme_{}'.format(count-1)])[0]:
                        rhyme_poem.append(j)
                        break
        else:
            print("无法找到韵脚全部相同的诗句！")

        print("-----------------*********-----------------")
        print("\n".join(rhyme_poem))
        print("-----------------*********-----------------")


    def head_and_tail(self,head_word,tail_word,flag):
        heads=list(head_word)
        tails=list(tail_word)
        names=locals()
        head_tail_poem=[]
        count=0
        for head in heads:
            names['poem_{}'.format(count)]=Poem.crawl(head+'开头的诗句',flag)
            for p in names['poem_{}'.format(count)]:
                if p[-1]==tails[count]:
                    head_tail_poem.append(p)
                    break
            count+=1
        print("-----------------*********-----------------")
        print("\n".join(head_tail_poem))
        print("-----------------*********-----------------")

if __name__=='__main__':

    Poem=Poem_Crawl()

    while 1:
        head_or_tail=input("请选择模式（1是藏头，0是藏尾,2是藏头且藏尾）：")
        if int(head_or_tail)==2:
            head_word=input("请输入您想要藏头的句子：")
            tail_word=input("请输入您想要藏尾的句子：")
            flag=input("请选择诗句长度（1是七言，0是五言）：")
            Poem.head_and_tail(head_word, tail_word, int(flag))
        else:
            head_word=input("请输入您想要藏头或藏尾的句子：")
            flag=input("请选择诗句长度（1是七言，0是五言）：")
            if int(head_or_tail):
                rhyme=input("请选择是否押韵（1为押韵，0为不押）：")
                if int(rhyme):
                    Poem.generate_rhyme(head_word,int(flag))
                else:
                    Poem.generate_poem(head_word,int(flag),int(head_or_tail))
            else:
                Poem.generate_poem(head_word, int(flag), int(head_or_tail))
