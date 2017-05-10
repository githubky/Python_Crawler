import pymysql
import re

class mysql:

    def __init__(self,host,user,password,database):
        self.db = pymysql.connect(host=host, user=user, password=password, database=database)
        self.cursor = self.db.cursor()

    def __del__(self):
        self.db.close()

    def Execute(self,sqlString):
        try:
            self.cursor.execute(sqlString)
            self.db.commit()
        except:
            print(sqlString)

    def ClearTable(self,tableName):
        sql="DELETE FROM " + tableName
        self.Execute(sql)

    def Insert(self,tableName,Content):
        values=""
        for var in Content.keys():
            c = var
            values = values + self.TransferToSQL(Content[var]) + ','
        values=values[:-1] #去除最后的逗号
        sql = 'INSERT INTO ' + tableName + '(' + ",".join(Content.keys()) + ' ) VALUES ( ' + values +')'

        self.Execute(sql)

    def Update(self, tableName, Content ,**key):
        cs = ""
        for var in Content.keys():
            c = var
            value=self.TransferToSQL(Content[var])
            c = c + ' = ' + value + ','
            cs = cs + c
        cs = cs[:-1]  # 去除最后的逗号

        if not key: #非空为True，即为空
            sql = 'UPDATE ' + tableName + ' SET ' + cs
        else:
            rs=""
            for var in key.keys():
                c = var
                value=self.TransferToSQL(key[var])
                c = c + ' = ' + value + ' and '
                rs = rs + c
            rs = rs[:-4]  # 去除最后的"and "
            sql = 'UPDATE ' + tableName + ' SET ' + cs + ' WHERE ' + rs

        self.Execute(sql)

    def InsertOrUpdate(self,tableName, Content ,**key):
        if not key: #非空为True，即为空
            self.Insert(tableName, Content)
        else:
            rs=""
            for var in key.keys():
                c = var
                value=self.TransferToSQL(key[var])
                c = c + ' = ' + value + ' and '
                rs = rs + c
            rs = rs[:-4]  # 去除最后的"and "
            sql = 'SELECT * FROM ' + tableName + ' WHERE ' + rs
            self.Execute(sql)
            if self.cursor.rowcount>0: #记录已存在
                self.Update(tableName, Content, **key)
            else:
                self.Insert(tableName, Content)

    def TransferToSQL(self,txt):
        if type(txt) == int:
            txt = str(txt)
        else:
            txt = re.sub(r">\s+<", "><", txt)
            txt = re.sub('\"', '\\\"', txt)
            txt='"' + txt + '"'

        return txt