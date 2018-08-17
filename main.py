import pandas as pd
import numpy as np
import os
from dataset import DataSetGenerator
from Label import LabelGenerator
from Csv import CsvGenerator
import tensorflow as tf
from keras import Sequential
from keras.layers import *
from keras.optimizers import *


file_site = 'H:\Wechat\WeChat Files\hhufjdd\Files\AI&FintechLab 2018 Material\SH600637'
stock_id = 'SH600637'
file_list = os.listdir(file_site)
CsvGenerator.generate_csv2(file_site)

f = open(file_site + '/' + file_list[9], 'r')
raw_data = pd.read_csv(f)
raw_data = raw_data[raw_data.close > 0]

for ind in range(10, 14):
    f = open(file_site + '/' + file_list[ind], 'r')
    raw_data1 = pd.read_csv(f)
    raw_data = raw_data[raw_data.close > 0]
    raw_data = pd.concat([raw_data, raw_data1])

col_name = raw_data.columns.tolist()
# col_name.insert(1, 'test')
# print(col_name)
# raw_data.reindex(columns=col_name)
raw_data['test'] = raw_data['price'] + raw_data['close']
test = raw_data.pop('test')
raw_data.insert(1, 'test', test)

raw_data.pop('time')

raw_data.to_csv('H:\Wechat\WeChat Files\hhufjdd\Files\AI&FintechLab 2018 Material\Data\database_5days_1min.csv', header=True, index=False)

# file_site = 'H:\Wechat\WeChat Files\hhufjdd\Files\AI&FintechLab 2018 Material\Data'
# f = open('H:\Wechat\WeChat Files\hhufjdd\Files\AI&FintechLab 2018 Material\Data\database_SH600637.csv')
# raw_data = pd.read_csv(f)
# raw_data['5min'] = raw_data['5min'] - raw_data['close']
# raw_data['10min'] = raw_data['10min'] - raw_data['close']
# raw_data['20min'] = raw_data['20min'] - raw_data['close']
# raw_data.to_csv('H:\Wechat\WeChat Files\hhufjdd\Files\AI&FintechLab 2018 Material\Data\database.csv', header=True)

# file_site = 'H:\Wechat\WeChat Files\hhufjdd\Files\AI&FintechLab 2018 Material\SH600637'
# stock_id = 'SH600637'
# file_list = os.listdir(file_site)
# # LabelGenerator.generate_label2(file_site, stock_id, 9, 1, 0.009, 0.009, 200)
# for ind in range(10,14):
#     CsvGenerator.generate_csv1(file_site, stock_id, ind, 1)



# dg = DataSetGenerator()
# dg.generate_data_set3(file_site, stock_id, -1, 5)


# print(len(X))
# print(X[0])
# print(len(X[0]))
# print(X[1])
# print(len(X[1]))

# f = open(file_site + '/' + file_list[-1], 'r')
# raw_data = pd.read_csv(f)
# raw_data = raw_data[raw_data.close > 0]
# raw_data_length = len(raw_data)
# fg = FeatureGenerator(raw_data, file_list, file_site, stock_id)
# X = []
# X1 = []
# temp = []
# (bar_feature, feature_length) = fg.generate_x(0,2)
# temp = temp + bar_feature
# (bar_feature, feature_length) = fg.generate_x(4,2)
# temp = temp + bar_feature
# X=X+temp
# X1 = X1.append(temp)

#print(file_list[-1])
# print(type(fg.generate_x(0,2)[0]))
# print(fg.generate_x(0,2)[0])