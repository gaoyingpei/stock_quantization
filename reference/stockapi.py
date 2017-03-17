# coding=utf-8
# python version3.5
# git https://github.com/gaoyingpei/stock_quantization

__author__ = 'gaoyingpei'
# 原作者为 gaoyingpei

import tushare as ts
# tushare 用于爬取新浪股票数据
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.finance import candlestick_ohlc
# 用户作图
import pandas as pds
# 用户数据结构
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
    
    if len(time1) == 10:
        time1 = time1 + ' 00:00:00'
        time2 = time2 + ' 00:00:00'
    
    timeArray1 = time.strptime(time1, "%Y-%m-%d %H:%M:%S")
    timeArray2 = time.strptime(time2, "%Y-%m-%d %H:%M:%S")

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
def degree(c1, c2):
    return abs(100 * (c1 - c2) / c2)


# 获取指标对应中文
def quotaName(quota):
    nameList = {'close':'收盘价', 'open':'开盘价', 'high':'最高价', 'low':'最低价', 'date':'区间', 'ma':'均线'}
    return nameList[quota]

# 根据股票数据画出股票K线图
def kline(stock, key, start, end):
    baseData = stock[start:end]

    # 设置字体
    plt.rcParams['font.sans-serif'] = ['SimHei']
    # 设置负值可显示
    plt.rcParams['axes.unicode_minus'] = False

    fig = plt.figure()
    ax = plt.subplot2grid((1,1), (0,0))
    # 设置标签
    plt.xlabel(quotaName('date'))
    plt.ylabel(quotaName(key))
    # 设置标题
    plt.title(quotaName(key) + '走势图')
    # 设置格子背景
    plt.grid(True)
    # 设置坐标界限
    plt.ylim(0, 10)

    quotes = []
    for i in range(0,len(baseData.index)):
        closep, codep, highp, lowp, openp, volumep, datep = baseData.ix[i]
        # datep = str(datep)[0:4] + str(datep)[5:7] + str(datep)[8:10]
        strconverter = mdates.strpdate2num('%Y%m%d')
        print(strconverter(datep))
        quotes.append([datep, openp, highp, lowp, closep, volumep])
    
    print(ax)
    candlestick_ohlc(ax, quotes, width=0.6, colorup='r', colordown='g')
    # 做出K线图
    plt.plot(baseData[key])
    plt.show()


# pandas and matplotlib api
# pandas.read_csv()
# pds.apply()
# pds.describe()

# df = pd.read_json("510050.csv")
# df.set_index('date') # df.index = df['date'].tolist()
# df['date'] = df.index
# stock.loc[start:end, ['date']]

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
    stock = pds.read_json('D:/Python/test/ma/000001.json').set_index('date')
    stock['date'] = stock.index
    kline(stock, 'close', '2013-01-01', '2014-01-01')