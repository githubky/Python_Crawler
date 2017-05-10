#coding=utf-8

from QCZJ import QCZJ
from Database  import mysql

def BuildSQLDict(attrs,obj):
    dict={}
    for attr in attrs:
        dict[attr]=getattr(obj,attr)
    return dict

url="http://club.autohome.com.cn/bbs/thread-c-2980-23423800-5.html"
#url="http://club.autohome.com.cn/bbs/thread-c-2980-62784220-1.html"

url='http://club.autohome.com.cn/bbs/thread-o-200223-61255063-1.html'

qczj=QCZJ(url)

db=mysql(host='127.0.0.1',user="root",password='123456',database="mycrawel")

# db.ClearTable('帖子')
# db.ClearTable('用户')
# db.ClearTable('帖子内容')

keysname=('网址','来源论坛', '标题', '点击', '回复')
t=BuildSQLDict(keysname,qczj)
db.InsertOrUpdate("帖子",t, 网址=t['网址'])

keysname=('id', '发帖', '回帖', '地区', '所属车会', '注册时间', '用户名', '签名', '精华帖', '荣誉', '认证车主', '车型')
for u in qczj.Users.keys():
    t=BuildSQLDict(keysname,qczj.Users[u])
    db.InsertOrUpdate("用户",t, id=t['id'])


keysname=('网址','内容', '发表时间', '来源', '楼层', '用户id')
for c in qczj.Contents:
    t=BuildSQLDict(keysname,c)
    db.InsertOrUpdate("帖子内容",t, 网址=t['网址'],楼层=t['楼层'])

del db
