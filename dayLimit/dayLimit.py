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
            '&start=20170101&end=20180818&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
            # '&end=20161231&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
            # 收盘价 最高价 最低价 开盘价 前收盘 涨跌额 涨跌幅 换手率 成交量 成交金额 总市值 流通市值 成交笔数
        else:
            url = 'http://quotes.money.163.com/service/chddata.html?code=1'+code+\
            '&start=20170101&end=20180818&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
        urllib.request.urlretrieve(url,'D:/files/'+code+'.csv') # 可以加一个参数dowmback显示下载进度

# 获取股票数据
def getStockData(allCodelist):
    # 循环读取每支股票的CSV文件获取每日信息
    result = {}
    for code in allCodelist:
        with open('D:/files/'+code+'.csv','r', encoding='gbk') as f:
            stockData = csv.reader(f)

            for one in stockData:
                if one[0] == '日期' or one[9] == 'None':
                    continue
                
                thisDate = one[0]

                if thisDate not in result:
                    result[thisDate] = []
                
                result[thisDate].append({'date':one[0], 'code':one[1][1:7], 'p':float(one[9])})
        
    # 获取日期倒序
    dates = sorted(result.keys(), reverse=True)

    # 循环读取每日信息
    lastResult = []
    for d in dates:
        # 单日排序
        result[d].sort(key=lambda x:x['p'], reverse=True)

        if result[d][25]['p'] >= 9.9: continue

        cnt = 0
        str = []
        for oneday in result[d]:
            if oneday['p'] >= 9.9:
                cnt = cnt + 1
                str.append(oneday['code'])
                continue
            break

        lastResult.append([d, cnt, "'" + ','.join(str)])
    
    return lastResult

# 存储为excel格式
def excelDownload(dateList):
    # 将今日涨幅统计追加到每日统计列表中
    result = DataFrame(np.array(dateList).reshape(len(dateList), 3),\
                            index=None,\
                            columns=['date','raising limit count','raising limit list'])
    
    # 保存为excel
    result.to_csv('D:/files/涨停统计.csv')

if __name__ == '__main__':
    allCodelist = getStockList()
    # downloadQfqStock(allCodelist)

    # 日排行
    dateList = getStockData(allCodelist)
    excelDownload(dateList)