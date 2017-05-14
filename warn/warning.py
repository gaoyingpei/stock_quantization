# coding=utf-8
# python version3.5
# git https://github.com/gaoyingpei/stock_quantization
# schtasks /create /tn "name" /tr "cmd /c python d:\1.bat" /sc daily /st 17:00

__author__ = 'gaoyingpei'
# 原作者为 gaoyingpei

import wx
import os

import matplotlib.pyplot as plt
from PIL import Image
# begin wxGlade: extracode
# end wxGlade


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.totalAmount = wx.TextCtrl(self, -1, "总仓位(万)",style=wx.TE_READONLY)
        self.todayPercent = wx.TextCtrl(self, -1, "今天可投入比例(%)",style=wx.TE_READONLY)
        self.todayAmount = wx.TextCtrl(self, -1, "今天投入资金(万)",style=wx.TE_READONLY)
        
        filename = './cache/rest.txt'
        totalA = ''
        percentA = ''
        if os.path.exists(filename):
            file = open(r'./cache/rest.txt', 'r')
            totalA = file.readline()
            percentA = file.readline()
            file.close()
            
        self.total = wx.TextCtrl(self, -1, totalA,style=wx.TE_CENTRE)
        self.percent = wx.TextCtrl(self, -1, percentA,style=wx.TE_CENTRE)
        self.amount = wx.TextCtrl(self, -1, "",style=wx.TE_CENTRE)
        self.warning = wx.Button(self, -1, "判断预警")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.warn, self.warning)
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
        filename = './cache/rest.txt'
        if not os.path.exists(filename):
            #os.remove(filename)
            file = open('./cache/rest.txt', 'w')
            file.write(self.total.GetValue())
            file.write("\n")
            file.write(self.percent.GetValue())
            file.close()

        self.warnFlg = float(self.total.GetValue()) * float(self.percent.GetValue()) / 100 - float(self.amount.GetValue())

        f = open(r'./cache/status.txt', 'w')
        f.truncate()
        f.write(str(self.warnFlg))
        f.close()

        if self.warnFlg < 0:
            img=Image.open('./img/红字.PNG')
            plt.figure("限额警告", figsize=(30,8))
            plt.imshow(img)
            plt.show()
        else:
            wx.MessageBox("可继续投入", "允许", wx.OK | wx.ICON_INFORMATION)

        event.Skip()

# end of class MyFrame
if __name__ == "__main__":
    app=wx.App(False)
    myframe=MyFrame(None)
    app.MainLoop()
