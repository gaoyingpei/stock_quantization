import os
filename = './cache/status.txt'
if os.path.exists(filename):
    os.remove(filename)

filename2 = './cache/rest.txt'
if os.path.exists(filename2):
    os.remove(filename2)
