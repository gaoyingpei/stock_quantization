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


# 下载股票列表
def getStockList():
    path = 'D:/Python/test/stocklist.csv'
    fq = ts.get_stock_basics()
    stockList = []
    stockList = pds.DataFrame(fq, columns=['timeToMarket', 'name'])
    stockList.to_csv(path, header=None)

# 下载数据(前复权)
def downloadQfqStock():
    # 读取CSV文件获取股票列表
    with open('D:/Python/test/stocklist.csv','r', encoding='utf-8') as f:
        stockList = csv.reader(f)
        for onestock in stockList:

            # 股票未上市
            if onestock[1] == '0':
                continue

            # 获取股票历史数据
            startTime = onestock[1][0:4] + '-' + onestock[1][4:6] + '-' + onestock[1][6:8]
            stock = ts.get_h_data(onestock[0], start=startTime)
            # 读取/存入本地JSON文件
            filename = 'D:/Python/test/stockQfq/' + onestock[0] + '.json'
            stock.to_json(filename, orient='records') #保存为JSON格式

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