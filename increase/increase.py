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
import wx

class MyFrame(wx.Frame):  
    def __init__(self, *args, **kwds):  
        # begin wxGlade: MyFrame.__init__  
        kwds["style"] = wx.DEFAULT_FRAME_STYLE  
        wx.Frame.__init__(self, *args, **kwds)  
        self.stockList = wx.Button(self, -1, "下载股票列表")
        self.stockToday = wx.Button(self, -1, "下载并统计今日股票涨幅")  
        self.path = './stock/'
  
        self.__set_properties()  
        self.__do_layout()  
  
        self.Bind(wx.EVT_BUTTON, self.getList, self.stockList)
        self.Bind(wx.EVT_BUTTON, self.getToday, self.stockToday)
        # end wxGlade  
        self.Show(True)  
  
    def __set_properties(self):  
        # begin wxGlade: MyFrame.__set_properties  
        self.SetTitle("统计每天股票涨幅")  
        self.stockList.SetMinSize((400, 100))  
        self.stockToday.SetMinSize((400, 100))  
        # end wxGlade  
  
    def __do_layout(self):  
        # begin wxGlade: MyFrame.__do_layout  
        sizer_1 = wx.BoxSizer(wx.VERTICAL)  
        grid_sizer_1 = wx.GridSizer(2, 1, 0, 0)  
        grid_sizer_1.Add(self.stockList, 0, 0, 0)  
        grid_sizer_1.Add(self.stockToday, 0, 0, 0)  
        sizer_1.Add(grid_sizer_1, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)  
        sizer_1.Fit(self)  
        self.Layout()  
        # end wxGlade  

    def getList(self, event):  # wxGlade: MyFrame.<event_handler>  
        # 创建文件夹
        path = self.path.rstrip("\\")
        if not os.path.exists(path):
            os.makedirs(path)
        
        fq = ts.get_stock_basics()
        stockList = []
        stockList = pds.DataFrame(fq, columns=['timeToMarket'])
        stockList.to_csv(self.path + 'stockList.csv', header=None)

        wx.MessageBox("股票列表下载完成", "download success" ,wx.OK | wx.ICON_INFORMATION)
        event.Skip()

    def getToday(self, event):  # wxGlade: MyFrame.<event_handler> 
        # 获取当前日期 
        startTime = time.strftime('%Y-%m-%d',time.localtime(time.time()))

        if not os.path.exists(self.path + 'stockList.csv'):
            wx.MessageBox("请先下载股票列表", "download error" ,wx.OK | wx.ICON_ERROR)
            return

        fileName = self.path + startTime + '.csv'
        resultFile = self.path + '每日统计.csv'

        cntArray = [0 for i in range(22)]
        rangeArray = [9.5, 9.0, 8.0, 7.0, 6.0, 5.0, 4.0, 3.0, 2.0, 1.0, 0, -1.0, -2.0, -3.0, -4.0, -5.0, -6.0, -7.0, -8.0, -9.0, -9.5]
        total = 0
        oneLimitUp = 0
        oneLimitDown = 0
        # 读取CSV文件获取股票列表
        with open(self.path + 'stockList.csv', 'r', encoding='utf-8') as f:
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
                        break
                    elif (increase <= rangeArray[20] and stock.open[0] == stock.close[0]):
                        oneLimitDown += 1
                        break
                    elif (i == 0 and increase >= rangeArray[i]):
                        cntArray[i] += 1
                        break
                    elif (i == len(rangeArray)-1 and increase < rangeArray[-1]):
                        cntArray[i+1] += 1
                        break
                    elif (i > 0 and i < len(rangeArray)-1 and increase >= rangeArray[i] and increase < rangeArray[i-1]):
                        cntArray[i] += 1
                        break

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

        wx.MessageBox("统计完成", "download success" ,wx.OK | wx.ICON_INFORMATION)
        event.Skip()


# end of class MyFrame  
if __name__ == "__main__":  
    app=wx.App(False)  
    myframe=MyFrame(None)  
    app.MainLoop()
