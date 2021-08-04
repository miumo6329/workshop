import os
import re

target = '..\\mp3'
for root, dirs, files in os.walk(target):
    for name in files:
        # print(root, name)
        new_name = re.sub('\d\d\d\d', '', name)
        new_name = new_name.replace(' -  - Audio - ', '')
        os.rename(os.path.join(root, name), os.path.join(root, new_name))


