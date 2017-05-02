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
import wx

class MyFrame(wx.Frame):  
    def __init__(self, *args, **kwds):  
        # begin wxGlade: MyFrame.__init__  
        kwds["style"] = wx.DEFAULT_FRAME_STYLE  
        wx.Frame.__init__(self, *args, **kwds)  
        self.stockList = wx.Button(self, -1, "获取股票列表")
        self.stockToday = wx.Button(self, -1, "获取当天股票信息")  
        self.toExcel = wx.Button(self, -1, "统计信息并导出EXCEL")  
  
        self.__set_properties()  
        self.__do_layout()  
  
        self.Bind(wx.EVT_BUTTON, self.getList, self.stockList)
        self.Bind(wx.EVT_BUTTON, self.getToday, self.stockToday)
        self.Bind(wx.EVT_BUTTON, self.countAndExcel, self.toExcel)
        # end wxGlade  
        self.Show(True)  
  
    def __set_properties(self):  
        # begin wxGlade: MyFrame.__set_properties  
        self.SetTitle("Python Warning by GYP")  
        self.totalAmount.SetMinSize((200, 40))  
        self.total.SetMinSize((200, 40)) 
        self.todayPercent.SetMinSize((200, 40))  
        self.percent.SetMinSize((200, 40))  
        self.todayAmount.SetMinSize((200, 40))  
        self.amount.SetMinSize((200, 40))  
        self.warning.SetMinSize((10, 10))  
        # end wxGlade  
  
    def __do_layout(self):  
        # begin wxGlade: MyFrame.__do_layout  
        sizer_1 = wx.BoxSizer(wx.VERTICAL)  
        grid_sizer_1 = wx.GridSizer(3, 2, 0, 0)  
        grid_sizer_1.Add(self.totalAmount, 0, 0, 0)  
        grid_sizer_1.Add(self.total, 0, 0, 0)  
        grid_sizer_1.Add(self.todayPercent, 0, 0, 0)  
        grid_sizer_1.Add(self.percent, 0, 0, 0)  
        grid_sizer_1.Add(self.todayAmount, 0, 0, 0)  
        grid_sizer_1.Add(self.amount, 0, 0, 0)  
        sizer_1.Add(grid_sizer_1, 1, wx.EXPAND, 0)
        sizer_1.Add(self.warning, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)  
        sizer_1.Fit(self)  
        self.Layout()  
        # end wxGlade  

    def warn(self, event):  # wxGlade: MyFrame.<event_handler>  
        self.warnFlg = float(self.total.GetValue()) * float(self.percent.GetValue()) - float(self.amount.GetValue())

        if self.warnFlg < 0:
            img=Image.open('./img/红字.PNG')
            plt.figure("限额警告", figsize=(30,8))
            plt.imshow(img)
            plt.show()
        else:
            wx.MessageBox("可继续投入", "允许" ,wx.OK | wx.ICON_INFORMATION)

        event.Skip()
  
# end of class MyFrame  
if __name__ == "__main__":  
    app=wx.App(False)  
    myframe=MyFrame(None)  
    app.MainLoop()



