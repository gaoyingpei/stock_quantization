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
            '&start=20180101&end=20180820&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
            # '&end=20161231&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
            # 收盘价 最高价 最低价 开盘价 前收盘 涨跌额 涨跌幅 换手率 成交量 成交金额 总市值 流通市值 成交笔数
        else:
            url = 'http://quotes.money.163.com/service/chddata.html?code=1'+code+\
            '&start=20180101&end=20180820&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
        urllib.request.urlretrieve(url,'D:/files/'+code+'.csv') # 可以加一个参数dowmback显示下载进度

# 获取股票数据
def getStockData(allCodelist):
    # 循环读取每支股票的CSV文件获取每日信息
    result = []
    for code in allCodelist:
        stock = []
        with open('D:/files/'+code+'.csv','r', encoding='gbk') as f:
            stockData = csv.reader(f)

            for one in stockData:
                if one[0] == '日期':
                    continue
                stock.append(one)

        dataLen = len(stock)

        for index in range(dataLen):
            if stock[index][9] == 'None' or stock[index][3] == stock[index][6] or float(stock[index][9]) < 9.9 or float(stock[index][9]) > 10.1:
                continue
            
            if index == 0 or stock[index-1][9] == 'None':
                nextOpen = 'None'
            else:
                nextOpen = stock[index-1][6]
            
            result.append({'date':stock[index][0], 'code':stock[index][1][1:7], 'close':float(stock[index][3]), 'nextOpen':nextOpen})

    # 循环读取每日信息
    lastResult = {'limitCnt':len(result), 'limitUp':0, 'limitDown':0, 'limitUpTotalRate':0, 'limitDownTotalRate':0, 'haltCnt':0, 'flatCnt':0}
    for one in result:
        if one['nextOpen'] == 'None':
            lastResult['haltCnt'] += 1
            continue
        
        one['nextOpen'] = float(one['nextOpen'])
        if one['nextOpen'] > one['close']:
            lastResult['limitUp'] += 1
            lastResult['limitUpTotalRate'] += (one['nextOpen'] - one['close']) / one['close']
        elif one['nextOpen'] < one['close']:
            lastResult['limitDown'] += 1
            lastResult['limitDownTotalRate'] += (one['nextOpen'] - one['close']) / one['close']
        else:
            lastResult['flatCnt'] += 1
    
    print('****** 非一字涨停后次日开盘价数据统计结果 *******')
    print('*** 涨停板 总数：' + str(lastResult['limitCnt']))
    print('*** 次日停牌 总数：' + str(lastResult['haltCnt']))
    print('*** 次日平开 总数：' + str(lastResult['flatCnt']))
    print('*** 次日高开 总数：' + str(lastResult['limitUp']) + '*** 高开率：' + str(lastResult['limitUp']*100/lastResult['limitCnt']) + '% ***')
    print('*** 次日低开 总数：' + str(lastResult['limitDown']) + '*** 低开率：' + str(lastResult['limitDown']*100/lastResult['limitCnt']) + '% ***')
    print('*** 次日高开 开盘价总收益率：' + str(lastResult['limitUpTotalRate']*100) + '% *** 开盘价平均收益率：' + str(lastResult['limitUpTotalRate']*100/lastResult['limitUp']) + '% ***')
    print('*** 次日低开 开盘价总收益率：' + str(lastResult['limitDownTotalRate']*100) + '% *** 开盘价平均收益率：' + str(lastResult['limitDownTotalRate']*100/lastResult['limitDown']) + '% ***')
    print('******************** end **********************\n')

if __name__ == '__main__':
    allCodelist = getStockList()
    # downloadQfqStock(allCodelist)

    getStockData(allCodelist)