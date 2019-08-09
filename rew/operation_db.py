"""
dict项目用于处理数据
"""
import pymysql
import hashlib

#　编写功能类　提供给服务端使用
class Database:
    def __init__(self,host = 'localhost',
                 port = 3306,
                 user='test',
                 passwd = '123654',
                 database = 'dict',
                 charset = 'utf8'):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.database = database
        self.charset = charset
        self.connect_db()  #　链接数据库

    def connect_db(self):
        self.db = pymysql.connect(host = self.host,
                                  port = self.port,
                                  user = self.user,
                                  passwd = self.passwd,
                                  database = self.database,
                                  charset = self.charset)

    # 创建游标
    def create_cursor(self):
        self.cur = self.db.cursor()

    #　关闭数据库
    def close(self):
        self.cur.close()
        self.db.close()

    #　处理注册
    def register(self,name,passwd):
        sql = "select * from user where name='%s'"%name
        self.cur.execute(sql)
        r = self.cur.fetchone()  #　如果查询到结果
        if r:
            return False

        #　加密处理
        hash = hashlib.md5((name+"the-salt").encode())
        hash.update(passwd.encode())
        sql="insert into user (name,passwd,dig) values (%s,%s,%s)"

        try:
            self.cur.execute(sql,[name,hash.hexdigest()],'none')
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False

    def login(self,name,passwd):
        sql = "select * from user where name='%s'" % name
        self.cur.execute(sql)
        r = self.cur.fetchone()
        if r:
            hash = hashlib.md5((name + "the-salt").encode())
            hash.update(passwd.encode())
            if hash.hexdigest()==r.passwd:
                return True
            else:
                return False
        else:
            return False

    def add(self,name,dig):
        sql='update set user dig=dig where name=name'
        self.cur.execute(sql)
        self.db.commit()
