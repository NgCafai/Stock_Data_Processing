import pandas as pd
import numpy as np
import csv
import os

file_site = 'H:\Wechat\WeChat Files\hhufjdd\Files\AI&FintechLab 2018 Material\SH600637'
file_list = os.listdir(file_site)
f = open(file_site + '/' + file_list[9], 'r')
raw_data = pd.read_csv(f)
# delete the useless data
raw_data = raw_data[raw_data.close > 0]

# concatenate five csv into one
for ind in range(10, 14):
    f = open(file_site + '/' + file_list[ind], 'r')
    raw_data1 = pd.read_csv(f)
    raw_data = raw_data[raw_data.close > 0]
    raw_data = pd.concat([raw_data, raw_data1])

raw_data = raw_data[raw_data.price > 0.1]
raw_data.to_csv(r'H:\Wechat\WeChat Files\hhufjdd\Files\AI&FintechLab 2018 Material\Data\5days_raw_data.csv', header=True, index=False)