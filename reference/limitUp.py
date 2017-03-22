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
            stock = ts.get_hist_data(value[0])
            # 读取/存入本地JSON文件
            filename = 'D:/Python/test/stock/' + value[0] + '.json'
            stock.to_json(filename, orient='records') #保存为JSON格式


# 统计所有股票涨停信息
def getLimitUp():
    stockCount = 0 #统计股票数
    totalCount = 0 #涨停次数
    redCount = 0 #涨停第二天上升次数
    greenCount = 0 #涨停第二天下跌次数
    redAferRed = 0 #涨停后第二天收阳第三天也收阳
    redAferGreen = 0 #涨停后第二天收阳第三天收阴
    greenAferRed = 0 #涨停后第二天收阴第三天也收阳
    greenAferGreen = 0 #涨停后第二天收阴第三天收阴
    limitWithoutOneLine = 0 #涨停，非一字板
    limitAfterLimitWithoutOneLine = 0 #连续涨停，非一字板
    limitupAfterDown = 0 #跌幅超过6%之后涨停次数
    ladWin = 0 #跌幅超过6%之后涨停之后10天内盈利次数
    ladLose = 0 #跌幅超过6%之后涨停之后10天内亏损次数
    rangeWin = 0 #跌幅超过6%之后涨停之后10天内盈利幅度
    rangeLose = 0 #跌幅超过6%之后涨停之后10天内亏损幅度

    # 读取CSV文件获取股票列表
    with open('D:/Python/test/stocklist.csv','r', encoding='utf-8') as csvfile:
        stockList = csv.reader(csvfile)
        for value in stockList:
            # 股票未上市
            if value[1] == '0':
                continue
            stockCount += 1
            # 读取JSON文件获取股票信息
            filename = 'D:/Python/test/stock/' + value[0] + '.json'
            jsonfile = open(filename, encoding='utf-8')
            stock = json.load(jsonfile)
            
            # 统计股票涨停信息
            addCnt = getOneCount(stock)

            # 追加次数
            totalCount += addCnt['total']
            redCount += addCnt['red']
            greenCount += addCnt['green']

            redAferRed += addCnt['rAr']
            greenAferRed += addCnt['gAr']
            redAferGreen += addCnt['rAg']
            greenAferGreen += addCnt['gAg']

            limitWithoutOneLine += addCnt['limit']
            limitAfterLimitWithoutOneLine += addCnt['lAl']

            limitupAfterDown += addCnt['lAd']
            ladWin += addCnt['ladWin']
            ladLose += addCnt['ladLose']
            rangeWin += addCnt['rWin']
            rangeLose += addCnt['rLose']
        
    print('******************** start ********************')
    # print('统计股票数：' + str(stockCount))
    # print('涨停总数：' + str(totalCount))
    # print('******************** Day1 *********************')
    # print('涨停=>收阳 总数：' + str(redCount))
    # print('涨停=>收阴 总数：' + str(greenCount))
    # print('涨停=>收阳 概率：' + str(redCount/totalCount))
    # print('涨停=>收阴 概率：' + str(greenCount/totalCount))
    # print('******************** Day2 *********************')
    # print('涨停=>收阳=>收阳 总数：' + str(redAferRed))
    # print('涨停=>收阳=>收阴 总数：' + str(greenAferRed))
    # print('涨停=>收阴=>收阳 总数：' + str(redAferGreen))
    # print('涨停=>收阴=>收阴 总数：' + str(greenAferGreen))
    # print('涨停=>收阳=>收阳 概率：' + str(redAferRed/redCount))
    # print('涨停=>收阳=>收阴 概率：' + str(greenAferRed/redCount))
    # print('涨停=>收阴=>收阳 概率：' + str(redAferGreen/greenCount))
    # print('涨停=>收阴=>收阴 概率：' + str(greenAferGreen/greenCount))
    # print('******************** 连续涨停 *********************')
    # print('涨停 总数：' + str(limitWithoutOneLine))
    # print('涨停=>涨停 概率：' + str(limitAfterLimitWithoutOneLine/limitWithoutOneLine))
    print('****** 大跌后涨停价买入10天后收盘价卖出胜率 *******')
    print('大跌6%=>涨停 总数：' + str(limitupAfterDown))
    print('大跌6%=>涨停=>10日后收盘价平仓 胜率：' + str(ladWin/limitupAfterDown))
    print('大跌6%=>涨停=>10日后收盘价平仓 平均升幅：' + str(rangeWin/ladWin))
    print('大跌6%=>涨停=>10日后收盘价平仓 平均跌幅：' + str(rangeLose/ladLose))
    print('大跌6%=>涨停=>10日后收盘价平仓 投入100000可盈利：' + str(100000 * (rangeWin/ladWin) * (ladWin/limitupAfterDown) - 100000 * abs(rangeLose/ladLose) * (ladLose/limitupAfterDown)) + '元')
    # print('大跌6%=>涨停=>10日后收盘价平仓 每次投入100000总盈利：' + str(100000 * (rangeWin/ladWin) * ladWin - 100000 * abs(rangeLose/ladLose) * ladLose) + '元')
    print('******************** end **********************\n')


# 获取单支股票统计数
def getOneCount(stock):
    limitUpFlg = 0 # 前天涨停
    totalCount = 0 #涨停次数
    redCount = 0 #涨停第二天上升次数
    greenCount = 0 #涨停第二天下跌次数
    redAferRed = 0 #涨停后第二天收阳第三天也收阳
    redAferGreen = 0 #涨停后第二天收阳第三天收阴
    greenAferRed = 0 #涨停后第二天收阴第三天也收阳
    greenAferGreen = 0 #涨停后第二天收阴第三天收阴
    limitWithoutOneLine = 0 #涨停，非一字板
    limitAfterLimitWithoutOneLine = 0 #连续涨停，非一字板
    newMarketDay = 0 #新上市经过日期
    limitupAfterDown = 0 #跌幅超过6%之后涨停次数
    ladWin = 0 #跌幅超过6%之后涨停之后10天内盈利次数
    ladLose = 0 #跌幅超过6%之后涨停之后10天内亏损次数
    rangeWin = 0 #跌幅超过6%之后涨停之后10天内盈利幅度
    rangeLose = 0 #跌幅超过6%之后涨停之后10天内亏损幅度

    # 未复权数据接口(对应函数get_hist_data)
    for i in range(len(stock)-1, 0, -1):
        # 排除新上市100天(70个工作日)
        newMarketDay += 1
        if newMarketDay <= 70:
            continue

        # 排除股票上市当天，停牌，停牌后复牌
        if (i >= len(stock) - 5 or stock[i]['open'] == 0 or stock[i + 5]['close'] == 0):
            continue

        # 下跌幅度超过6%
        if (stock[i + 11]['p_change'] < -6 and stock[i + 10]['p_change'] >= 9.5 and stock[i + 10]['p_change'] < 12):
            # 排除涨停一字板
            if stock[i + 9]['low'] != stock[i + 9]['high']:
                limitupAfterDown += 1
                buyPrice = stock[i + 9]['open']
                sellPrice = stock[i]['close']
                # 排除跌停一字板
                for j in range(i, -1, -1):
                    if ((stock[j]['p_change'] > -9.5 and stock[j]['low'] != stock[j]['high']) or j == 0):
                        sellPrice = stock[j]['close']
                        break

                buyRange = (sellPrice - buyPrice) / buyPrice - 0.002
                if buyRange >= 0:
                    ladWin += 1
                    rangeWin += buyRange
                else:
                    ladLose += 1
                    rangeLose += buyRange

        # 涨停
        limitUpFlg = 1 if (9.5 <= stock[i + 2]['p_change'] and stock[i + 2]['p_change'] < 12) else 0
        if limitUpFlg == 1:
            totalCount += 1
        # 连续涨停，非一字板
        if limitUpFlg == 1 and (stock[i + 2]['close'] - stock[i + 2]['open']) / stock[i + 2]['open'] > 0.01:
            limitWithoutOneLine += 1
            if (9.5 <= stock[i + 1]['p_change'] and stock[i + 1]['p_change'] < 12) and\
                ((stock[i + 1]['close'] - stock[i + 1]['open']) / stock[i + 1]['open'] > 0.01):
                limitAfterLimitWithoutOneLine += 1
        # 昨天涨停并且当天收阳
        if (stock[i + 1]['p_change'] > 0 and limitUpFlg == 1):
            redCount += 1
            # 前天涨停并且当天收阳
            if (stock[i]['p_change'] > 0):
                redAferRed += 1
            # 前天涨停并且当天收阴
            if (stock[i]['p_change'] < 0):
                greenAferRed += 1
        # 昨天涨停并且当天收阴
        if (stock[i + 1]['p_change'] < 0 and limitUpFlg == 1):
            greenCount += 1
            # 前天涨停并且当天收阳
            if (stock[i]['p_change'] > 0):
                redAferGreen += 1
            # 前天涨停并且当天收阴
            if (stock[i]['p_change'] < 0):
                greenAferGreen += 1

    return {'red':redCount, 'green':greenCount, 'total':totalCount,\
            'rAr':redAferRed, 'gAr':greenAferRed, 'rAg':redAferGreen,\
            'gAg':greenAferGreen, 'limit':limitWithoutOneLine, 'lAl':limitAfterLimitWithoutOneLine,\
            'lAd':limitupAfterDown, 'ladWin':ladWin, 'ladLose':ladLose, 'rWin':rangeWin, 'rLose':rangeLose}


if __name__ == '__main__':  
    # downloadStockList()
    # downloadStockData()
    getLimitUp()