import os
filename = './cache/status.txt'
if os.path.exists(filename):
    os.remove(filename)