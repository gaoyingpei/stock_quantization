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
            '&start=20100101&end=20171231&fields=VOTURNOVER;VATURNOVER'
            # '&end=20161231&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
        else:
            url = 'http://quotes.money.163.com/service/chddata.html?code=1'+code+\
            '&start=20100101&end=20171231&fields=VOTURNOVER;VATURNOVER'
        urllib.request.urlretrieve(url,'D:/Python/test/qfq/'+code+'.csv') # 可以加一个参数dowmback显示下载进度

# 获取股票数据
def getStockData(allCodelist):
    # 循环读取每支股票的CSV文件获取每日信息
    result = {}
    for code in allCodelist:
        with open('D:/Python/test/qfq/'+code+'.csv','r', encoding='gbk') as f:
            stockData = csv.reader(f)

            for one in stockData:
                if one[0] == '日期':
                    continue
                
                thisDate = one[0]
                if thisDate not in result:
                    result[thisDate] = []
                
                result[thisDate].append({'date':one[0], 'code':one[1][1:7], 'name':one[2], 'vol':one[3], 'amount':float(one[4]), 'close':one[5], 'percent':one[6]})
        
    # 获取日期倒序
    dates = sorted(result.keys(), reverse=True)

    # 循环读取每日信息
    lastResult = []
    for d in dates:
        # 单日排序
        result[d].sort(key=lambda x:x['amount'], reverse=True)

        # 取前10名
        topTen = result[d][:10]

        # 转化成数组，固定元素的顺序
        for one in topTen:
            lastResult.append([one['date'], one['code'], one['name'], one['vol'], one['amount'], one['close'], one['percent']])
    
    return lastResult

# 存储为excel格式
def excelDownload(dateList):
    # 将今日涨幅统计追加到每日统计列表中
    result = DataFrame(np.array(dateList).reshape(len(dateList), 7),\
                            index=None,\
                            columns=['日期','股票代码','股票名称','成交量','成交额','收盘价','当日涨幅'])
    
    # 保存为excel
    result.to_csv('D:/Python/test/成交额日统计.csv')

# 获取股票数据
def getStockDataMonth(allCodelist):
    # 循环读取每支股票的CSV文件获取每日信息
    result = {}
    for code in allCodelist:
        with open('D:/Python/test/qfq/'+code+'.csv','r', encoding='gbk') as f:
            stockData = csv.reader(f)

            for one in stockData:
                if one[0] == '日期':
                    continue
                
                spl = one[0].split('-')
                thisMonth = spl[0] + '年' + spl[1] + '月'

                if thisMonth not in result:
                    result[thisMonth] = []
                
                isExist = 0
                for i in range(0, len(result[thisMonth]), 1):
                    if result[thisMonth][i]['code'] == code:
                        isExist = 1
                        result[thisMonth][i]['vol'] = float(result[thisMonth][i]['vol']) + float(one[3])
                        result[thisMonth][i]['amount'] = float(result[thisMonth][i]['amount']) + float(one[4])
                        break

                if isExist == 0:
                    result[thisMonth].append({'date':thisMonth, 'code':one[1][1:7], 'name':one[2], 'vol':one[3], 'amount':float(one[4])})
        
    # 获取日期倒序
    dates = sorted(result.keys(), reverse=True)

    # 循环读取每日信息
    lastResult = []
    for d in dates:
        # 单日排序
        result[d].sort(key=lambda x:x['amount'], reverse=True)

        # 取前20名
        topTwn = result[d][:20]

        # 转化成数组，固定元素的顺序
        for one in topTwn:
            lastResult.append([one['date'], one['code'], one['name'], one['vol'], one['amount']])
    
    return lastResult

# 存储为excel格式
def excelDownloadMonth(dateList):
    # 将今日涨幅统计追加到每日统计列表中
    result = DataFrame(np.array(dateList).reshape(len(dateList), 5),\
                            index=None,\
                            columns=['月份','股票代码','股票名称','成交量','成交额'])
    
    # 保存为excel
    result.to_csv('D:/Python/test/成交额月统计.csv')

# 获取股票数据
def getStockDataYear(allCodelist):
    # 循环读取每支股票的CSV文件获取每日信息
    result = {}
    for code in allCodelist:
        with open('D:/Python/test/qfq/'+code+'.csv','r', encoding='gbk') as f:
            stockData = csv.reader(f)

            for one in stockData:
                if one[0] == '日期':
                    continue
                
                thisYear = one[0].split('-')[0]

                if thisYear not in result:
                    result[thisYear] = []
                
                isExist = 0
                for i in range(0, len(result[thisYear]), 1):
                    if result[thisYear][i]['code'] == code:
                        isExist = 1
                        result[thisYear][i]['vol'] = float(result[thisYear][i]['vol']) + float(one[3])
                        result[thisYear][i]['amount'] = float(result[thisYear][i]['amount']) + float(one[4])
                        break

                if isExist == 0:
                    result[thisYear].append({'date':thisYear, 'code':one[1][1:7], 'name':one[2], 'vol':float(one[3]), 'amount':float(one[4])})
        
    # 获取日期倒序
    dates = sorted(result.keys(), reverse=True)

    # 循环读取每日信息
    lastResult = []
    for d in dates:
        # 单日排序
        result[d].sort(key=lambda x:x['amount'], reverse=True)

        # 取前20名
        topTwn = result[d][:20]

        # 转化成数组，固定元素的顺序
        for one in topTwn:
            lastResult.append([one['date'], one['code'], one['name'], one['vol'], one['amount']])
    
    return lastResult

# 存储为excel格式
def excelDownloadYear(dateList):
    # 将今日涨幅统计追加到每日统计列表中
    result = DataFrame(np.array(dateList).reshape(len(dateList), 5),\
                            index=None,\
                            columns=['年份','股票代码','股票名称','成交量','成交额'])
    
    # 保存为excel
    result.to_csv('D:/Python/test/成交额年统计.csv')

if __name__ == '__main__':
    allCodelist = getStockList()
    # downloadQfqStock(allCodelist)

    # # 日排行
    # dateList = getStockData(allCodelist)
    # excelDownload(dateList)

    # # 月排行
    # dateList = getStockDataMonth(allCodelist)
    # excelDownloadMonth(dateList)

    # 年排行
    dateList = getStockDataYear(allCodelist)
    excelDownloadYear(dateList)
