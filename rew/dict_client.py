"""
dict 客户端
发起请求，展示结果
"""

from socket import *
from getpass import getpass
import requests
from bs4 import BeautifulSoup
ADDR = ('127.0.0.1', 8000)
# 　所有函数都用ｓ
s = socket()
# s.connect(ADDR)


# 二级界面
def login(name):
    while True:
        print("""
        ================Query=================
         1. 查书单    2. 历史记录　　　3. 注销
        ======================================
        """)
        cmd = input("输入选项:")
        if cmd == '1':
            search(name)
        elif cmd == '2':
            pass
        elif cmd == '3':
            return
        else:
            print("请输入正确命令!")
# 查书单
def search(name):
    req=requests.get('https://book.douban.com/top250?icn=index-book250-all')
    obj=BeautifulSoup(req.content,'html.parser')
    b_list=obj.find_all('table')
    b_dict={}
    for i in range(1,len(b_list)):
        final_list=BeautifulSoup(str(b_list[i]),'html.parser').select('a')
        b_dict[final_list[1].text.replace(' ','').replace('\n','')]=final_list[1].get('href')
    print(b_dict.keys())
    sel=input('请选择一本小说名:')
    if sel in b_dict.keys():
        req = requests.get(b_dict[sel])
        obj=BeautifulSoup(req.content,'html.parser')
        bb_list=obj.find_all('div',class_='review-list')
        ffinal_list=BeautifulSoup(str(BeautifulSoup(str(bb_list[0]),'html.parser').select('h2')[0]),'html.parser').select('a')[0]
        print(ffinal_list.get('href'))
        rreq=requests.get(ffinal_list.get('href'))
        # print(rreq.content.decode())
        title=ffinal_list.text
        content=BeautifulSoup(str(BeautifulSoup(rreq.content,'html.parser').find_all('div',class_='main')[0]),'html.parser').find_all('div',class_='main-bd')[0].text

        print(('标题:%s\n内容:%s')%(title,content),end='\n\n')
        msg=('标题:%s\n内容:%s')%(title,content)
        ch=input("是否加入收藏夹?(请输入是或者否）")
        if ch=='是':
            msg='m'+'=-=name=-='+msg
            s.send(msg.encode())
        else:
            search(name)
    else:
        print('请输入正确书名')
        search(name)






# 注册
def do_register():
    while True:
        name = input("User:")
        passwd = input('passward:')
        passwd1 = input('passward:')

        if (' ' in name) or (' ' in passwd):
            print("用户名或密码不能有空格")
            continue
        if passwd != passwd1:
            print("两次密码不一致")
            continue

        msg = "R %s %s" % (name, passwd)
        # 　发送请求
        s.send(msg.encode())
        # 　接收反馈
        data = s.recv(128).decode()
        if data == 'OK':
            print("注册成功")
            login(name)
        else:
            print("注册失败")
        return


# 处理登录
def do_login():
    name = input("User:")
    passwd = getpass()
    msg = "L %s %s" % (name, passwd)
    s.send(msg.encode())
    # 　等待反馈
    data = s.recv(128).decode()
    if data == 'OK':
        print("登录成功")
        login(name)
    else:
        print("登录失败")
def do_exit():
    s.send('quit'.encode())

# 创建网络链接
def main():
    while True:
        print("""
        ================Welcome===============
         1. 注册       　2. 登录　　　　 3. 退出
        ======================================
        """)
        cmd = input("输入选项:")
        if cmd == '1':
            do_register()
        elif cmd == '2':
            do_login()
        elif cmd == '3':
            do_exit()
        else:
            print("请输入正确命令!")


if __name__ == "__main__":
    # main()
    search('dscfd')