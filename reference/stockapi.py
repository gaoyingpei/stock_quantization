# coding=utf-8
# python version3.5
# git https://github.com/gaoyingpei/stock_quantization

__author__ = 'gaoyingpei'
# 原作者为 gaoyingpei

import tushare as ts
# tushare 用于爬取新浪股票数据
import pandas as pds
import json
import csv
import time


# 下载股票列表
def downloadStockList():
    fq = ts.get_stock_basics()
    stockList = []
    stockList = pds.DataFrame(fq, columns=['timeToMarket'])
    stockList.to_csv('D:/Python/test/stocklist.csv', header=None)


# 下载数据
def downloadStockData():
    # 读取CSV文件获取股票列表
    with open('D:/Python/test/stocklist.csv','r', encoding='utf-8') as f:
        stockList = csv.reader(f)
        for value in stockList:
            # 股票未上市
            if value[1] == '0':
                continue
            # 获取股票历史数据
            startTime = value[1][0:4] + '-' + value[1][4:6] + '-' + value[1][6:8]
            stock = ts.get_k_data(code=value[0], ktype='D', autype='qfq', start=startTime)
            # 读取/存入本地JSON文件
            filename = 'D:/Python/test/ma/' + value[0] + '.json'
            stock.to_json(filename, orient='records') #保存为JSON格式


# 一线法主流程
def oneMa():
    test = 1


# 返回距离当前时间多少小时之前的时间
def beforeTime(hours):
    hours = int(hours)
    t = time.time() - hours*60*60
    t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))
    return t


# 返回两个时间间隔的天数(format='20141010' || '2014-10-10')
def intervalDay(time1, time2):
    # '20141010'类型转换
    if len(time1) == 8:
        time1 = time1[0:4] + '-' + time1[4:6] + '-' + time1[6:8]
        time2 = time2[0:4] + '-' + time2[4:6] + '-' + time2[6:8]
    
    timeArray1 = time.strptime(time1 + ' 16:00:00', "%Y-%m-%d %H:%M:%S")
    timeArray2 = time.strptime(time2 + ' 16:00:00', "%Y-%m-%d %H:%M:%S")

    # 两个时间间隔秒数
    seconds = abs(time.mktime(timeArray2) - time.mktime(timeArray1))

    return int(seconds/86400)


# 生成指定指标在某一范围内的均线数据
def MA(stock, key, day):
    for i in range(0, len(stock)):
        start = i + 1 - day if i + 1 - day >= 0 else 0
        stock[i]['MA' + str(day)] = sum(oneDay[key] for oneDay in stock[start:i+1]) / day

    return stock


# 生成指定指标在某一范围内的最大值
def HHV(stock, key, day, index):
    start = index + 1 - day if index + 1 - day >= 0 else 0
    high = max(value[key] for value in stock[start:index + 1])

    for i in range(start, index+1):
        if stock[i][key] == high:
            return stock[i]


# 生成指定指标在某一范围内的最小值
def LLV(stock, key, day, index):
    start = index + 1 - day if index + 1 - day >= 0 else 0
    low = min(value[key] for value in stock[start:index + 1])

    for i in range(start, index+1):
        if stock[i][key] == low:
            return stock[i]

# 生成指定指标在某一天前几天的值
def REF(stock, key, day, index):
    start = index + 1 - day if index + 1 - day >= 0 else 0
    return stock[start][key]


# 获取两个值偏离幅度
def degree(c1, c2)
    return abs(100 * (c1 - c2) / c2)


# 根据股票数据画出股票K线图
def kline(stock, key, start, end):
    

# pandas and matplotlib api
# pandas.read_csv()
# pds.apply()
# pds.describe()

# plt.plot()
# plt.show()
# plt.rcParams[]
# plt.xlim()
# plt.ylim()
# plt.xticks()
# plt.yticks()
# plt.title()
# plt.xlabel()
# plt.ylabel()
# plt.grid()
# plt.legend()
# plt.subplot()

# plt.bar()
# plt.barh()
# plt.hist()
# plt.pie()
# plt.boxplot()

# plt.figure()
# ax = fig.add.axes()
# ax.plot()
# ax.set_title()
# ax.set_xlim()
# ...



if __name__ == '__main__':  
    # downloadStockList()
    # downloadStockData()