# import http.client
# http_client = http.client.HTTPConnection('www.cqdehua.cn',80,timeout=10)
# http_client.request('get','/recharge/referer.html')
# response = http_client.getresponse()
# print(response.status)
# print(response.read())

import urllib.request #发生请求用的插件
from bs4 import BeautifulSoup #解析html用的插件
import cx_Oracle as cx #链接oracle用的插件
import sys


# output=sys.stdout
# outputfile=open("printlog.txt","a",encoding='utf-8') #打开一个文件用于记录所有的print
# sys.stdout=outputfile
# type = sys.getfilesystemencoding()#python编码转换到系统编码输出
try:
    # # response = urllib.request.urlopen('http://www.cqdehua.cn/recharge/referer.html')
    response = urllib.request.urlopen('http://tieba.baidu.com/f?kw=p2p&ie=utf-8')
    print(response.status)
    content = response.read().decode('UTF-8')
    print(content)
    response.close()

    soup = BeautifulSoup(content,"html.parser")

    conn = cx.connect('ZZQ/ZZQZZQ@120.76.132.101:1521/orcl2', encoding = "UTF-8", nencoding = "UTF-8")   #用自己的实际数据库用户名、密码、主机ip地址 替换即可

    print(len(soup.find("ul",{"id":"thread_list"}).find_all('li')))
    for li in soup.find("ul",{"id":"thread_list"}).find_all('li'):
        try:
            print(li.name)
            print(li['class'])
            link = li.find("div",{"class":"threadlist_lz"}).find("div",{"class":"threadlist_title"}).find("a")
            time = li.find("div",{"class":"threadlist_detail"}).find("div",{"class":"threadlist_author"}).find("span",{"class":"threadlist_reply_date"}).get_text()

        except :
            print("异常发生了")
            continue
            link = li.find("div",{"class":"threadlist_lz clearfix"}).find("div",{"class":"threadlist_title"}).find("a")
            print("异常发生了:%s" % link['class'])
            continue
        title = link.get_text()
        url = "http://tieba.baidu.com"+link.get("href")
        id = link.get("href")[3:]
        print("id: %s title：%s 发布时间: %s " % (id,title ,time))

        sql="INSERT into REPTILE_POST (type,post_id,post_content) values (225410,"+id+" ,'"+title+"')" #插入p2p相关的帖子sql语句
        print(sql)
        curs=conn.cursor()
        try:
            curs.execute (sql)
            conn.commit()
        except:
            pass
        response = urllib.request.urlopen("http://tieba.baidu.com/p/"+id)
        content = response.read().decode('UTF-8')
        response.close()
        soup = BeautifulSoup(content, "html.parser")
        print("-------找打cc的个数",len(soup.find_all("cc")))
        for cc in soup.find_all("cc"):
            text = cc.find("div").get_text().strip()
            print(text)
            sql = "INSERT into REPTILE_POST_REPLY (post_id,reply_content) values (" + id + " ,'" + text + "')"  # 插入p2p相关的帖子的回复sql语句
            curs = conn.cursor()
            try:
                curs.execute(sql)
                conn.commit()
            except:
                pass
        # curs.commit
        # curs.close
    #sql='SELECT * FROM APP_AUTODO_RESULT' #sql语句

    # for result in curs:
    #     print(result)

    # row=curs.fetchone()
    # print(row[0])

    conn.close()
except Exception as e:
    print(e)
    # print("url：%s" % url)


    # html = getContent(url)
    # soup2 = BeautifulSoup(html,"html.parser")
    # content = soup2.find("div",{"id":"content"}).get_text()
    # print("content:%s" % content)

# import urllib3
# response = urllib3.PoolManager().request('get','http://www.cqdehua.cn/recharge/referer.html')
# print(response.status)

# import  requests
# response = requests.get('http://www.cqdehua.cn/recharge/referer.html')
# print(response.status_code)
# print(response.text)
# print(response.json())
# print(response.reason)