from bs4 import BeautifulSoup
import re

from Web import WebCode

class QCZJ:
    soup=""
    Users={};
    Contents=[];

    网址=""
    来源论坛=""
    标题=""
    点击=-1
    回复=-1

    def __init__(self,URL):
        self.网址=URL
        webcode = WebCode()
        webcode.getWebCode(URL)
        self.soup = BeautifulSoup(webcode.text, 'lxml')

        self.getSummary()

        for i in range(self.getMaxPage()):
            URL=re.search(r'(.*)\d+.html',URL).group(1)+str(i+1)+".html"
            webcode.getWebCode(URL)
            self.soup = BeautifulSoup(webcode.text, 'lxml')
            self.getOnePage()

    def getSummary(self):
        p = self.soup.find(name='div', attrs={"class": "consnav","id":"consnav"})
        self.点击 = p.find(name='font', attrs={"id": "x-views"}).string
        self.回复 = p.find(name='font', attrs={"id": "x-replys"}).string
        self.来源论坛 = p.find(name='a').string
        self.标题 = p.findAll(name='span')[-1].string

    def getOnePage(self):
        users={};
        contents=[];
        UC = self.soup.findAll(name='div', attrs={"class":"clearfix contstxt outer-section"})
        for p in UC:
            u=self.getOneUser(p)
            users[u.id]=u
            c=self.getOneContent(p)
            contents.append(c)
        self.Users.update(users)
        self.Contents.extend(contents)

    def getOneUser(self,p):
        user=用户()
        user.id = p.get("uid")
        user.用户名=p.find(name='a', attrs={"xname": "uname"}).string
        if p.find(name='a', attrs={"class": "crade"}) is None:
            user.认证车主=0
        else:
            user.认证车主=1

        t= p.findAll(name="li")

        s=""
        for st in t[5].stripped_strings:
            s=s+st
        user.精华帖 = int(re.search(r"\d+", s).group())

        s=""
        for st in t[6].stripped_strings:
            s=s+st
        user.发帖 = int(re.search(r"(\d+)帖", s).group(1))
        user.回帖 = int(re.search(r"(\d+)回", s).group(1))

        user.注册时间 =re.search(r"\d+年\d+月\d+日", t[7].string).group()

        s = ""
        for st in t[8].stripped_strings:
            s = s + st
        user.地区=re.search(r"来自：(.+)", s).group(1)

        index=9 #记录“车型”所在的编号
        s = ""
        for st in t[9].stripped_strings:
            s = s + st
        if re.search("所属",s) is not None:
            user.所属车会=re.search("所属：(.+)",s).group(1)
            index=10

        user.车型 = t[index].findAll(name='a')[-1].get("title")

        s=""
        for tt in t[index+1].findAll(name='h2'):
            s=s+tt.string+"|"
        user.荣誉 = s

        t=p.find('div',attrs={'class':'c999 plr25 mb5'})
        if t is not None:
            user.签名=re.search(r'签名：\s*(.+)',t.string).group(1)

        return user

    def getOneContent(self,p):
        content=帖子()
        content.网址=self.网址
        content.用户id = p.get("uid")

        t=p
        p=t.find(name="div",attrs={"class":"conright fl"})
        if p is not None:
            content.发表时间=p.find("span",attrs={"xname":'date'}).string

            t=p.find("span",attrs={"xname":'date'}).next_sibling.find('a')
            if type(t) is not int:
                content.来源=t.string

            content.楼层=p.find('button',attrs={ 'style':"box-sizing: content-box;color: #3b5998;" ,'title':"复制本楼链接到剪贴板"}).get('rel')

            content.内容=str(p.find('div',attrs={'class':"x-reply font14",'xname':"content"}))

        else:
            p = t.find(name="div", attrs={"class": "conright fr"})

            content.发表时间 = p.find("span", attrs={"xname": 'date'}).string

            t = p.find("span", attrs={"xname": 'date'}).next_sibling.find('a')
            if type(t) is not int:
                content.来源 = t.string

            content.楼层 = p.find('button', attrs={'style': "box-sizing: content-box;color: #3b5998;", 'title': "复制帖子链接到剪贴板"}).get('rel')

            content.内容 = str(p.find('div', attrs={'class': "conttxt", 'xname': "content"}))

        return content

    def getMaxPage(self):
        return int(self.soup.find('div',attrs={'class':'pages','id':'x-pages2'}).get("maxindex"))

class 用户:
    id=""
    用户名=""
    认证车主=-1
    #当前帮助值=-1
    精华帖=-1
    发帖=-1
    回帖=-1
    注册时间=""
    地区=""
    所属车会=""
    车型=""
    荣誉=""
    签名 = ""

class 帖子:
    网址=""
    用户id=""
    发表时间 = ""
    来源 = ""
    楼层 = -1
    内容 = ""

