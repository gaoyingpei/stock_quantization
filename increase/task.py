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
import csv
import time
import os

def getList(path):  # wxGlade: MyFrame.<event_handler>  
    # 创建文件夹
    path = path.rstrip("\\")
    if not os.path.exists(path):
        os.makedirs(path)
    
    fq = ts.get_stock_basics()
    stockList = []
    stockList = pds.DataFrame(fq, columns=['timeToMarket'])
    stockList.to_csv(path + 'stockList.csv', header=None)

def getToday(path):  # wxGlade: MyFrame.<event_handler> 
    # 获取当前日期 
    startTime = time.strftime('%Y-%m-%d',time.localtime(time.time()))

    if not os.path.exists(path + 'stockList.csv'):
        return

    fileName = path + startTime + '.csv'
    resultFile = path + '每日统计.csv'

    cntArray = [0 for i in range(22)]
    rangeArray = [9.5, 9.0, 8.0, 7.0, 6.0, 5.0, 4.0, 3.0, 2.0, 1.0, 0, -1.0, -2.0, -3.0, -4.0, -5.0, -6.0, -7.0, -8.0, -9.0, -9.5]
    total = 0
    oneLimitUp = 0
    oneLimitDown = 0
    # 读取CSV文件获取股票列表
    with open(path + 'stockList.csv', 'r', encoding='utf-8') as f:
        stockList = csv.reader(f)
        for value in stockList:
            # 股票未上市
            if value[1] == '0':
                continue
            # 获取股票历史数据
            stock = ts.get_hist_data(value[0], start = startTime, end = startTime)
            if (stock.values.shape[0] == 0):
                continue 
            
            total += 1
            stock['code'] = value[0]
            # 读取/存入本地CSV文件
            if os.path.exists(fileName):
                stock.to_csv(fileName, mode='a', header=None)
            else:
                stock.to_csv(fileName)
            
            # 判断涨幅范围
            increase = float('%.2f' % stock.p_change[0])
            for i in range(0, len(rangeArray), 1):
                if (increase >= rangeArray[0] and stock.open[0] == stock.close[0]):
                    oneLimitUp += 1
                elif (increase <= rangeArray[20] and stock.open[0] == stock.close[0]):
                    oneLimitDown += 1
                elif (i == 0 and increase >= rangeArray[i]):
                    cntArray[i] += 1
                elif (i == len(rangeArray)-1 and increase < rangeArray[-1]):
                    cntArray[i+1] += 1
                elif (i > 0 and i < len(rangeArray)-1 and increase >= rangeArray[i] and increase < rangeArray[i-1]):
                    cntArray[i] += 1

    cntArray.insert(0, oneLimitDown)
    cntArray.insert(0, oneLimitUp)
    cntArray.insert(0, total)
    # 将今日涨幅统计追加到每日统计列表中
    todayData = DataFrame(np.array(cntArray).reshape(1, 25),\
                            index=[startTime],\
                            columns=['合计','一字涨停','一字跌停','[9.5～]','[9.0～9.5)','[8.0～9.0)','[7.0～8.0)','[6.0～7.0)',\
                                        '[5.0～6.0)','[4.0～5.0)','[3.0～4.0)','[2.0～3.0)','[1.0～2.0)',\
                                        '[0～1.0)','[-1.0～0)','[-2.0～-1.0)','[-3.0～-2.0)','[-4.0～-3.0)','[-5.0～-4.0)',\
                                        '[-6.0～-5.0)','[-7.0～-6.0)','[-8.0～-7.0)','[-9.0～-8.0)','[-9.5～-9.0)','[～-9.5)'])
    # 本地有数据则追加一条，无数据则新建一条
    if os.path.exists(resultFile):
        todayData.to_csv(resultFile, mode='a', header=None)
    else:
        todayData.to_csv(resultFile)


# end of class MyFrame  
if __name__ == "__main__":  
    path = './stock/'
    # getList(path)
    getToday(path)
