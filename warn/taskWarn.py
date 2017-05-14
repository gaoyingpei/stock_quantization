# coding=utf-8
# python version3.5
# git https://github.com/gaoyingpei/stock_quantization
# schtasks /create /tn "name" /tr "cmd /c python d:\1.bat" /sc daily /st 17:00

__author__ = 'gaoyingpei'
# 原作者为 gaoyingpei

import matplotlib.pyplot as plt
from PIL import Image

# end of class MyFrame
if __name__ == "__main__":
    f = open(r'./cache/status.txt', 'r')
    rest = f.read()

    if float(rest) < 0:
        img=Image.open('./img/红字.PNG')
        plt.figure("限额警告", figsize=(30,8))
        plt.imshow(img)
        plt.show()

    f.close()

