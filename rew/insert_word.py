import pymysql
import re

f = open('dict.txt')
db = pymysql.connect('localhost', 'root',
                     '123456', 'dict')
cur = db.cursor()

sql = 'insert into words (word,mean) \
VALUES (%s,%s)'

for line in f:
    # 　获取匹配内容元组　(word,mean)
    tup = re.findall(r'(\w+)\s+(.*)', line)[0]

    try:
        cur.execute(sql, tup)
        db.commit()
    except Exception:
        db.rollback()

f.close()
cur.close()
db.close()
