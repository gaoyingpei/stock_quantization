import time
import requests
# import urllib.request

def value_get():
    for i in range(0, 100):
        result = requests.get("https://m.1768.com/?act=game_mnzdd&st=get_chest_point")
        print(eval(result.text)['point'])
        # stdout = urllib.request.urlopen("https://m.1768.com/?act=game_mnzdd&st=get_chest_point")
        # stdoutInfo = stdout.read().decode('gb2312')
        # print(eval(stdoutInfo))
        time.sleep(1)


if __name__ == '__main__':
    value_get()
