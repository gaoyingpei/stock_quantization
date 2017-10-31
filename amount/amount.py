# coding=utf-8
# python version3.5
# git https://github.com/gaoyingpei/stock_quantization

__author__ = 'gaoyingpei'
# 原作者为 gaoyingpei

import tushare as ts
# tushare 用于爬取新浪股票数据
import pandas as pds
from pandas import DataFrame
import numpy as np
import json
import csv
import datetime as dt
import urllib.request
import re


# 下载股票列表
def getStockList():
    allCodeList = []
    html = urllib.request.urlopen('http://quote.eastmoney.com/stocklist.html').read()
    html = html.decode('gbk')
    s = r'<li><a target="_blank" href="http://quote.eastmoney.com/\S\S(.*?).html">'
    pat = re.compile(s)
    code = pat.findall(html)
    for item in code:
        if item[0]=='6' or item[0]=='3' or item[0]=='0':
            allCodeList.append(item)
    return allCodeList

# 下载数据(前复权)
def downloadQfqStock(allCodelist):
    for code in allCodelist:
        print('正在获取%s股票数据...'%code)
        if code[0]=='6':
            url = 'http://quotes.money.163.com/service/chddata.html?code=0'+code+\
            '&start=20151001&end=20171031&fields=VOTURNOVER;VATURNOVER'
            # '&end=20161231&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
        else:
            url = 'http://quotes.money.163.com/service/chddata.html?code=1'+code+\
            '&start=20151001&end=20171031&fields=VOTURNOVER;VATURNOVER'
        urllib.request.urlretrieve(url,'D:/Python/test/stockQfq/'+code+'.csv') # 可以加一个参数dowmback显示下载进度

        # test = requests.get("http://quotes.money.163.com/service/chddata.html?code=0601857&start=20151001&end=20171031&fields=VOTURNOVER;VATURNOVER")
        # test2 = test.text
        # test3 = test2.split('\r\n')

        # test4 = [{'date':'2017-10-31','code':601857,'name':'中国石油','vol':47719652,'amount':393957807.0},{'date':'2017-10-30','code':601857,'name':'中国石油','vol':101277166,'amount':835501367.0}]
        # test5 = np.array(test4)

# 获取股票数据
def getStockData():
    # 读取CSV文件获取股票列表
    with open('D:/Python/test/stocklist.csv','r', encoding='utf-8') as f:
        stockList = csv.reader(f)
        stockData = []
        for onestock in stockList:
            # 读取JSON文件获取股票信息
            filename = 'D:/Python/test/stockQfq/' + onestock[0] + '.json'
            jsonfile = open(filename, encoding='utf-8')

            temp = {}
            temp[onestock[0]] = (json.load(jsonfile)).reverse() # 按时间倒序
            stockData.append(temp)

        return stockData

# 统计所有股票成交额信息
def sumStock(stockData):
    today = dt.datetime.now()

    # 读取CSV文件获取股票列表
    with open('D:/Python/test/stocklist.csv','r', encoding='utf-8') as f:
        stockList = csv.reader(f)
        dateList = []

        # 循环获取两年数据
        for i in range(730):
            # 获取要检查的日期
            ymd = today - dt.timedelta(days=i)
            oneDay = {}
            oneDay[ymd] = []
            
            # 循环每支股票
            for onestock in stockList:
                # 循环单支股票所有日期
                for val in stockData[onestock[0]]:
                    if val['date'] == ymd:
                        oneDay[ymd].append({'code':onestock[0], 'name':onestock[2], 'date':ymd, 'amount':val['amount']})
                        break

            # 排序
            oneDay[ymd].sort(key = lambda x:x["amount"])

            # 取前10名
            dateList.append(oneDay[ymd][:10])
        
        return dateList.reverse()

# 存储为excel格式
def excelDownload(dateList):
    # 将今日涨幅统计追加到每日统计列表中
    result = DataFrame(np.array(dateList).reshape(len(dateList), 4),\
                            index=['date'],\
                            columns=['股票代码','股票名称','日期','成交额'])
    
    # 保存为excel
    result.to_excel('./stock/每日统计.csv')

if __name__ == '__main__':  
    getStockList()
    # downloadQfqStock()
    # stockData = getStockData()
    # dateList = sumStock(stockData)
    # excelDownload(dateList)