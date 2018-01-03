#coding:utf-8
import re
import json
import pandas
import requests
import urllib.request
import chardet
import webbrowser
import numpy as np
from datetime import datetime
from bs4 import BeautifulSoup
 
#提取网页正文，放入txt中
def remove_js_css (content):
    # """ remove the the javascript and the stylesheet and the comment content (<script>....</script> and <style>....</style> <!-- xxx -->) """
    r = re.compile(r'''<script.*?</script>''',re.I|re.M|re.S)
    s = r.sub ('',content)
    r = re.compile(r'''<style.*?</style>''',re.I|re.M|re.S)
    s = r.sub ('', s)
    r = re.compile(r'''<!--.*?-->''', re.I|re.M|re.S)
    s = r.sub('',s)
    r = re.compile(r'''<meta.*?>''', re.I|re.M|re.S)
    s = r.sub('',s)
    r = re.compile(r'''<ins.*?</ins>''', re.I|re.M|re.S)
    s = r.sub('',s)
    return s
 
def remove_empty_line (content):
    # """remove multi space """
    r = re.compile(r'''^\s+$''', re.M|re.S)
    s = r.sub ('', content)
    r = re.compile(r'''\n+''',re.M|re.S)
    s = r.sub('\n',s)
    return s
 
def remove_any_tag (s):
    s = re.sub(r'''<[^>]+>''','',s)
    return s.strip()
 
def remove_any_tag_but_a (s):
    text = re.findall (r'''<a[^r][^>]*>(.*?)</a>''',s,re.I|re.S|re.S)
    text_b = remove_any_tag (s)
    return len(''.join(text)),len(text_b)
 
def remove_image (s,n=50):
    image = 'a' * n
    r = re.compile (r'''<img.*?>''',re.I|re.M|re.S)
    s = r.sub(image,s)
    return s
 
def remove_video (s,n=1000):
    video = 'a' * n
    r = re.compile (r'''<embed.*?>''',re.I|re.M|re.S)
    s = r.sub(video,s)
    return s
 
def sum_max (values):
    cur_max = values[0]
    glo_max = -999999
    left,right = 0,0
    for index,value in enumerate (values):
        cur_max += value
        if (cur_max > glo_max) :
            glo_max = cur_max
            right = index
        elif (cur_max < 0):
            cur_max = 0
 
    for i in range(right, -1, -1):
        glo_max -= values[i]
        if abs(glo_max < 0.00001):
            left = i
            break
    return left,right+1
 
def method_1 (content, k=1):
    if not content:
        return None,None,None,None
    tmp = content.split('\n')
    group_value = []
    for i in range(0,len(tmp),k):
        group = '\n'.join(tmp[i:i+k])
        group = remove_image (group)
        group = remove_video (group)
        text_a,text_b= remove_any_tag_but_a (group)
        temp = (text_b - text_a) - 8 
        group_value.append (temp)
    left,right = sum_max (group_value)
    return left,right, len('\n'.join(tmp[:left])), len ('\n'.join(tmp[:right]))
 
def extract (content):
    content = remove_empty_line(remove_js_css(content))
    left,right,x,y = method_1 (content)
    return '\n'.join(content.split('\n')[left:right])
 
#输入url，将其新闻页的正文输入txt
def extract_news_content(web_url,file_name):  
    request = urllib.request.Request(web_url)  
   
    #在请求加上头信息，伪装成浏览器访问  
    request.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6')  
    opener = urllib.request.build_opener()  
    html= opener.open(request).read()
    infoencode = chardet.detect(html)['encoding']##通过第3方模块来自动提取网页的编码
    if html!=None and infoencode!=None:#提取内容不为空，error.或者用else
        html = html.decode(infoencode,'ignore')
        soup=BeautifulSoup(html)
        content=soup.renderContents()
        content_text=extract(content)#提取新闻网页中的正文部分，化为无换行的一段文字
        content_text= re.sub("&nbsp;"," ",content_text)
        content_text= re.sub("&gt;","",content_text)
        content_text= re.sub("&quot;",'""',content_text)
        content_text= re.sub("<[^>]+>","",content_text)
        content_text=re.sub("\n","",content_text)
        file = open(file_name,'a')#append
        file.write(content_text)
        file.close()
 
#抓取百度新闻搜索结果:中文搜索，前10页，url：key=关键词
def search(key_word):
    key_word = urllib.parse.quote(key_word)
    search_url='http://news.baidu.com/ns?word=%s&tn=news&from=news&cl=2&rn=20&ct=1'%(key_word)
    # print(search_url.replace('key_word',key_word))
    req=urllib.request.urlopen(search_url)
    real_visited=0
    for count in range(10):#前10页
        html=req.read()
        html=html.decode('utf8')
        soup=BeautifulSoup(html, 'lxml')  
        content  = soup.findAll("li", {"class": "result"}) #resultset object
        num = len(content)
        visited_url_list = []
        for i in range(num):
            #先解析出来所有新闻的标题、来源、时间、url
            p_str= content[i].find('a') #if no result then nontype object
            contenttitle=p_str.renderContents()
            contenttitle=contenttitle.decode('utf-8', 'ignore')#need it
            contenttitle= re.sub("<[^>]+>","",contenttitle)
            contentlink=str(p_str.get("href"))
            #存放顺利抓取的url，对比
            visited_url=open(r'D:\Python\test\visited-cn.txt','r')#是否已经爬过
            visited_url_list=visited_url.readlines()
            visited_url.close()#及时close
            exist=0
            for item in visited_url_list:
                if contentlink==item:
                    exist=1
            if exist!=1:#如果未被访问url
                p_str2= content[i].find('p').renderContents()
                contentauthor=p_str2[:p_str2.find("&nbsp;&nbsp")]#来源
                contentauthor=contentauthor.decode('utf-8', 'ignore')#时
                contenttime=p_str2[p_str2.find("&nbsp;&nbsp")+len("&nbsp;&nbsp")+ 1:]
                contenttime=contenttime.decode('utf-8', 'ignore')
                #第i篇新闻，filename="D:\\Python27\\newscn\\%d.txt"%(i)
                #file = open(filename,'w'),一个txt一篇新闻
                real_visited+=1
                file_name=r"D:\Python\test\newscn\%d.txt"%(real_visited)
                file = open(file_name,'w')
                file.write(contenttitle.encode('utf-8'))
                file.write(u'\n')
                file.write(contentauthor.encode('utf-8'))
                file.write(u'\n')
                file.write(contenttime.encode('utf-8'))
                file.write(u'\n'+contentlink+u'\n')
                file.close()
                extract_news_content(contentlink,file_name)#还写入文件
                visited_url_list.append(contentlink)#访问之
                visited_url=open(r'D:\Python\test\visited-cn.txt','a')#标记为已访问，永久存防止程序停止后丢失                
                visited_url.write(contentlink+u'\n')
                visited_url.close()
            if len(visited_url_list)>=120:
                break
            #解析下一页
        if len(visited_url_list)>=120:
            break
        if count==0:
            next_num=0
        else:
            next_num=1
        
        print(soup('a',{'href':True,'class':'n'}))
        next_page='http://news.baidu.com'+soup('a',{'href':True,'class':'n'})[next_num]['href'] # search for the next page#翻页
        print(next_page)
        req=urllib.request.urlopen(next_page)

# if __name__=='__main__':
#     key_word=input('input key word:')
#     search(key_word)



#############sina#################
def getHtml(page):#获取网址内容
    page=str(page)
    html=requests.get("http://search.sina.com.cn/?q=%E8%8C%85%E5%8F%B0&range=all&c=news&sort=time&page="+page).text
    return html

def getPage():#获得网页总数
    html=requests.get("http://search.sina.com.cn/?range=all&c=news&q=%E8%8C%85%E5%8F%B0&from=home").text   #网址
    soup=BeautifulSoup(''.join(html), 'lxml')
    a=soup('div',{ 'class' : 'l_v2' })
    race=[]
    c=""
    race=str(a).split("新闻")[1].split("篇")[0].split(",")   #获取网址有多少页码
    b=len(race)
    for i in range(b):
        c+=race[i]
    b=int(c)/20
    return b

def getContents(html):#获取指定新闻内容
    soup=BeautifulSoup(''.join(html), 'lxml')
    rs=re.compile("fgray_time")
    html=soup.findAll('span',attrs={'class':rs})
    rs=re.compile("box-result clearfix")
    contents=soup.findAll('div',attrs={'class':rs})
    for c in html:
        length=len(c.text.split(' '))
        if length==3:
                   source=c.text.split(' ')[0]#新闻来源
                   time=c.text.split(' ')[1]+' '+c.text.split(' ')[2]#新闻发表时间
                   print(source)
                   print(time)
        else:
                   time=c.text#新闻发表时间
                   source=''#新闻来源
                   print(time)


    for i in contents:
        title= i.h2.a.text#新闻标题
        content= i.p.text#新闻简介内容
        print(title)


# if __name__=="__main__":
#     count=getPage()
#     print(111)
#     for i in np.arange(0, count):
#         print(getContents(getHtml(i)))
#     print(222)


# 获取新闻的标题，内容，时间和评论数
def getNewsdetial(newsurl):
    res = requests.get(newsurl)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,'html.parser')
    newsTitle = soup.select('.page-header h1')[0].text.strip()
    nt = datetime.strptime(soup.select('.time-source')[0].contents[0].strip(),'%Y年%m月%d日%H:%M')
    newsTime = datetime.strftime(nt,'%Y-%m-%d %H:%M')
    newsArticle = getnewsArticle(soup.select('.article p'))
    newsAuthor = newsArticle[-1]
    return newsTitle,newsTime,newsArticle,newsAuthor
def getnewsArticle(news):
    newsArticle = []
    for p in news:
         newsArticle.append(p.text.strip())
    return newsArticle

# 获取评论数量

def getCommentCount(newsurl):
    m = re.search('doc-i(.+).shtml',newsurl)
    newsid = m.group(1)
    commenturl = 'http://comment5.news.sina.com.cn/page/info?version=1&format=js&channel=gn&newsid=comos-{}&group=&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=20'
    comment = requests.get(commenturl.format(newsid))   #将要修改的地方换成大括号，并用format将newsid放入大括号的位置
    jd = json.loads(comment.text.lstrip('var data='))
    return jd['result']['count']['total']


def getNewsLinkUrl():
#     得到异步载入的新闻地址（即获得所有分页新闻地址）
    urlFormat = 'http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=gnxw&cat_2==gdxw1||=gatxw||=zs-pl||=mtjj&level==1||=2&show_ext=1&show_all=1&show_num=22&tag=1&format=json&page={}&callback=newsloadercallback&_=1501000415111'
    url = []
    for i in range(1,10):
        res = requests.get(urlFormat.format(i))
        jd = json.loads(res.text.lstrip('  newsloadercallback(').rstrip(');'))
        url.extend(getUrl(jd))     #entend和append的区别
    return url

def getUrl(jd):
#     获取每一分页的新闻地址
    url = []
    for i in jd['result']['data']:
        url.append(i['url'])
    return url

# 取得新闻时间，编辑，内容，标题，评论数量并整合在total_2中
def getNewsDetial():
    title_all = []
    author_all = []
    commentCount_all = []
    article_all = []
    time_all = []
    url_all = getNewsLinkUrl()
    for url in url_all:
        title_all.append(getNewsdetial(url)[0])
        time_all.append(getNewsdetial(url)[1])
        article_all.append(getNewsdetial(url)[2])
        author_all.append(getNewsdetial(url)[3])
        commentCount_all.append(getCommentCount(url))
    total_2 = {'a_title':title_all,'b_article':article_all,'c_commentCount':commentCount_all,'d_time':time_all,'e_editor':author_all}
    return total_2

# # ( 运行起始点 )用pandas模块处理数据并转化为excel文档
# if __name__=="__main__":
#     df = pandas.DataFrame(getNewsDetial())
#     df.to_excel('news2.xlsx')


#commentsUrl用于获取新闻评论数等json信息
commentsUrl = 'http://comment5.news.sina.com.cn/page/info?version=1&format=js&channel=gn&newsid=comos-{}&group=&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=20&jsvar=loader_1487565938347_44362583'

#获取评论数量的函数
def getCommentsCount(newsUrl):
    before = re.escape('doc-i')
    after = re.escape('.shtml')
    m = re.search(before + '(.+)' + after, newsUrl)
    newsId = m.group(1)
    comments = requests.get(commentsUrl.format(newsId))
    jd = json.loads(comments.text.strip('var loader_1487565938347_44362583='))
    commentCount = jd['result']['count']['total']
    return commentCount

#获取新闻具体内容的函数
def getNewsDetail(newsUrl):
    result = {}
    res = requests.get(newsUrl)
    res.encoding = 'UTF-8'
    soup = BeautifulSoup(res.text,'html.parser')
    result['title'] = soup.select('#artibodyTitle')[0].text
    result['newsSource'] = source = soup.select('#navtimeSource span a')[0].text
    timesource = soup.select('#navtimeSource')[0].contents[0].strip()
    result['newsTime'] = datetime.strptime(timesource,'%Y年%m月%d日%H:%M')
    result['article'] = '\n'.join([p.text.strip() for p in soup.select('#artibody p')[:-1]])
    result['editor'] = soup.select('.article-editor')[0].text.strip('责任编辑：')
    result['commentsCount'] = getCommentsCount(newsUrl)
    return result

#测试
if __name__=="__main__":
    result = getNewsDetail('http://news.sina.com.cn/c/nd/2017-02-20/doc-ifyarrcf4846170.shtml')
    print(result)