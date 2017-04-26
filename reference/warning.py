import wx  
  
# begin wxGlade: extracode  
# end wxGlade  
  
  
class MyFrame(wx.Frame):  
    def __init__(self, *args, **kwds):  
        # begin wxGlade: MyFrame.__init__  
        kwds["style"] = wx.DEFAULT_FRAME_STYLE  
        wx.Frame.__init__(self, *args, **kwds)  
        self.text_ctrl_1 = wx.TextCtrl(self, -1, "",style=wx.TE_READONLY)  
        self.button_37 = wx.Button(self, -1, "1")  
        self.button_38 = wx.Button(self, -1, "2")  
        self.button_39 = wx.Button(self, -1, "3")  
        self.button_40 = wx.Button(self, -1, "+")  
        self.button_41 = wx.Button(self, -1, "4")  
        self.button_42 = wx.Button(self, -1, "5")  
        self.button_43 = wx.Button(self, -1, "6")  
        self.button_44 = wx.Button(self, -1, "-")  
        self.button_46 = wx.Button(self, -1, "7")  
        self.button_45 = wx.Button(self, -1, "8")  
        self.button_47 = wx.Button(self, -1, "9")  
        self.button_48 = wx.Button(self, -1, "x")  
        self.button_49 = wx.Button(self, -1, "C")  
        self.button_50 = wx.Button(self, -1, "0")  
        self.button_51 = wx.Button(self, -1, "=")  
        self.button_52 = wx.Button(self, -1, "/")  
  
        self.__set_properties()  
        self.__do_layout()  
  
        self.Bind(wx.EVT_BUTTON, self.bu1, self.button_37)  
        self.Bind(wx.EVT_BUTTON, self.bu2, self.button_38)  
        self.Bind(wx.EVT_BUTTON, self.bu3, self.button_39)  
        self.Bind(wx.EVT_BUTTON, self.bu_plus, self.button_40)  
        self.Bind(wx.EVT_BUTTON, self.bu4, self.button_41)  
        self.Bind(wx.EVT_BUTTON, self.bu5, self.button_42)  
        self.Bind(wx.EVT_BUTTON, self.bu6, self.button_43)  
        self.Bind(wx.EVT_BUTTON, self.bu_min, self.button_44)  
        self.Bind(wx.EVT_BUTTON, self.bu7, self.button_46)  
        self.Bind(wx.EVT_BUTTON, self.bu8, self.button_45)  
        self.Bind(wx.EVT_BUTTON, self.bu9, self.button_47)  
        self.Bind(wx.EVT_BUTTON, self.bu_mul, self.button_48)  
        self.Bind(wx.EVT_BUTTON, self.bu_clear, self.button_49)  
        self.Bind(wx.EVT_BUTTON, self.bu0, self.button_50)  
        self.Bind(wx.EVT_BUTTON, self.bu_result, self.button_51)  
        self.Bind(wx.EVT_BUTTON, self.bu_chu, self.button_52)  
        # end wxGlade  
        self.Show(True)  
  
    def __set_properties(self):  
        # begin wxGlade: MyFrame.__set_properties  
        self.SetTitle("Python Calculater by CYG")  
        self.text_ctrl_1.SetMinSize((400, 50))  
        self.button_37.SetMinSize((100, 50))  
        self.button_38.SetMinSize((100, 50))  
        self.button_39.SetMinSize((100, 50))  
        self.button_40.SetMinSize((100, 50))  
        self.button_41.SetMinSize((100, 50))  
        self.button_42.SetMinSize((100, 50))  
        self.button_43.SetMinSize((100, 50))  
        self.button_44.SetMinSize((100, 50))  
        self.button_46.SetMinSize((100, 50))  
        self.button_45.SetMinSize((100, 50))  
        self.button_47.SetMinSize((100, 50))  
        self.button_48.SetMinSize((100, 50))  
        self.button_49.SetMinSize((100, 50))  
        self.button_50.SetMinSize((100, 50))  
        self.button_51.SetMinSize((100, 50))  
        self.button_52.SetMinSize((100, 50))  
        # end wxGlade  
  
    def __do_layout(self):  
        # begin wxGlade: MyFrame.__do_layout  
        sizer_2 = wx.BoxSizer(wx.VERTICAL)  
        sizer_3 = wx.BoxSizer(wx.VERTICAL)  
        grid_sizer_1 = wx.GridSizer(4, 4, 0, 0)  
        sizer_3.Add(self.text_ctrl_1, 0, 0, 0)  
        grid_sizer_1.Add(self.button_37, 0, 0, 0)  
        grid_sizer_1.Add(self.button_38, 0, 0, 0)  
        grid_sizer_1.Add(self.button_39, 0, 0, 0)  
        grid_sizer_1.Add(self.button_40, 0, 0, 0)  
        grid_sizer_1.Add(self.button_41, 0, 0, 0)  
        grid_sizer_1.Add(self.button_42, 0, 0, 0)  
        grid_sizer_1.Add(self.button_43, 0, 0, 0)  
        grid_sizer_1.Add(self.button_44, 0, 0, 0)  
        grid_sizer_1.Add(self.button_46, 0, 0, 0)  
        grid_sizer_1.Add(self.button_45, 0, 0, 0)  
        grid_sizer_1.Add(self.button_47, 0, 0, 0)  
        grid_sizer_1.Add(self.button_48, 0, 0, 0)  
        grid_sizer_1.Add(self.button_49, 0, 0, 0)  
        grid_sizer_1.Add(self.button_50, 0, 0, 0)  
        grid_sizer_1.Add(self.button_51, 0, 0, 0)  
        grid_sizer_1.Add(self.button_52, 0, 0, 0)  
        sizer_3.Add(grid_sizer_1, 1, wx.EXPAND, 0)  
        sizer_2.Add(sizer_3, 1, wx.EXPAND, 0)  
        self.SetSizer(sizer_2)  
        sizer_2.Fit(self)  
        self.Layout()  
        # end wxGlade  
  
    def bu1(self, event):  # wxGlade: MyFrame.<event_handler>  
        self.text_ctrl_1.AppendText("1")  
        event.Skip()  
  
    def bu2(self, event):  # wxGlade: MyFrame.<event_handler>  
        self.text_ctrl_1.AppendText("2")  
        event.Skip()  
  
    def bu3(self, event):  # wxGlade: MyFrame.<event_handler>  
        self.text_ctrl_1.AppendText("3")  
        event.Skip()  
  
    def bu_plus(self, event):  # wxGlade: MyFrame.<event_handler>  
        self.num1=self.text_ctrl_1.GetValue()  
        self.op="+"  
        self.text_ctrl_1.Clear()  
        event.Skip()  
  
    def bu4(self, event):  # wxGlade: MyFrame.<event_handler>  
        self.text_ctrl_1.AppendText("4")  
        event.Skip()  
  
    def bu5(self, event):  # wxGlade: MyFrame.<event_handler>  
        self.text_ctrl_1.AppendText("5")  
        event.Skip()  
  
    def bu6(self, event):  # wxGlade: MyFrame.<event_handler>  
        self.text_ctrl_1.AppendText("6")  
        event.Skip()  
  
    def bu_min(self, event):  # wxGlade: MyFrame.<event_handler>  
        self.num1=self.text_ctrl_1.GetValue()  
        self.op="-"  
        self.text_ctrl_1.Clear()  
        event.Skip()  
  
    def bu7(self, event):  # wxGlade: MyFrame.<event_handler>  
        self.text_ctrl_1.AppendText("7")  
        event.Skip()  
  
    def bu8(self, event):  # wxGlade: MyFrame.<event_handler>  
        self.text_ctrl_1.AppendText("8")  
        event.Skip()  
  
    def bu9(self, event):  # wxGlade: MyFrame.<event_handler>  
        self.text_ctrl_1.AppendText("9")  
        event.Skip()  
  
    def bu_mul(self, event):  # wxGlade: MyFrame.<event_handler>  
        self.num1=self.text_ctrl_1.GetValue()  
        self.op="x"  
        self.text_ctrl_1.Clear()  
        event.Skip()  
  
    def bu_clear(self, event):  # wxGlade: MyFrame.<event_handler>  
        self.text_ctrl_1.Clear()  
        event.Skip()  
  
    def bu0(self, event):  # wxGlade: MyFrame.<event_handler>  
        self.text_ctrl_1.AppendText("0")  
        event.Skip()  
  
    def bu_chu(self, event):  # wxGlade: MyFrame.<event_handler>  
        self.num1=self.text_ctrl_1.GetValue()  
        self.op="/"  
        self.text_ctrl_1.Clear()  
        event.Skip()  
  
    def bu_result(self, event):  # wxGlade: MyFrame.<event_handler>  
        self.num2=self.text_ctrl_1.GetValue()  
        num1=int(self.num1)  
        num2=int(self.num2)  
        if self.op=="+":  
            self.text_ctrl_1.SetValue(str(num1+num2))  
        elif self.op=="-":  
            self.text_ctrl_1.SetValue(str(num1-num2))  
        elif self.op=="x":  
            self.text_ctrl_1.SetValue(str(num1*num2))  
        elif self.op=="/":  
            self.text_ctrl_1.SetValue(str(num1/num2))  
        event.Skip()  
  
  
# end of class MyFrame  
if __name__ == "__main__":  
  
    app=wx.App(False)  
    myframe=MyFrame(None)  
    app.MainLoop()