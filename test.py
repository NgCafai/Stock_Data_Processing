import pandas as pd
import numpy as np
import csv
import os
import math


def generate_csv2(file_site, step=1):
    """
    If the upper barrier is touched first, we label the observation as a 1.
    If the lower barrier is touched first, we label the observation as a -1.
    Otherwise, we label the observation as a 0.
    :param file_site: the exact directory of the csv file, eg.'H:\Wechat\WeChat Files\hhufjdd\Files\AI&FintechLab 2018 Material\SH600637'
    :param step:
    :return:
    """
    # 读取该股票的所有文件列表
    file_list = os.listdir(file_site)

    f = open(file_site + '/' + file_list[-5], 'r')
    raw_data = pd.read_csv(f)
    f.close()
    # delete the useless data
    raw_data = raw_data[raw_data.close > 0]

    # concatenate five csv into one
    for ind in range(-4, 0):
        f = open(file_site + '/' + file_list[ind], 'r')
        raw_data1 = pd.read_csv(f)
        f.close()
        raw_data = raw_data[raw_data.price > 0.1]
        raw_data = pd.concat([raw_data, raw_data1])

    raw_data = raw_data[raw_data.price > 0.1]

    # delete the useless columns
    col_name = raw_data.columns.tolist()
    for ind in range(1, 2):
        raw_data.pop(col_name[ind])
    for ind in range(6, 10):
        raw_data.pop(col_name[ind])
    for ind in range(45, 60):
        raw_data.pop(col_name[ind])

    # add some features
    raw_data['mid_price'] = (raw_data['buy1'] + raw_data['sale1']) / 2
    mid_price = raw_data.pop('mid_price')
    raw_data.insert(5, 'mid_price', mid_price)
    mid_price = raw_data.mid_price.tolist()

    col_name = raw_data.columns.tolist()
    col_name.insert(6, 'VW_Avg_buy_price')
    col_name.insert(7, 'VW_Avg_sale_price')
    col_name.insert(8, 'aggressor_side')
    col_name.insert(9, 'relative_buy_vol')
    col_name.insert(10, 'relative_sale_vol')
    col_name.insert(11, 'VW_Avg_price')
    col_name.insert(12, 'VW_Avg_price_minus_current_price')
    # create the csv file in which we are going to write the data
    csv_file = open('H:\Wechat\WeChat Files\hhufjdd\Files\AI&FintechLab 2018 Material\Data\database_SH600031_0820.csv', 'w', newline='')
    writer = csv.writer(csv_file)
    writer.writerow(col_name + ['next_vwap', 'next_delta', '30s_vwap', '30s_delta', 'mid_price_delta'])

    price = raw_data.price.tolist()
    vol = raw_data.vol.tolist()
    buy1 = raw_data.buy1.tolist()
    buy5 = raw_data.buy5.tolist()
    sale1 = raw_data.sale1.tolist()
    sale5 = raw_data.sale5.tolist()

    # transform raw_data to the type list
    raw_data_list = (np.array(raw_data)).tolist()
    raw_data_length = len(raw_data)

    # access some values to simplize the calculation of the features
    temp = raw_data
    temp['total_buy_vol'] = temp['bc1'] + temp['bc2'] + temp['bc3'] + temp['bc4'] + temp['bc5']
    temp['VM_Avg_buy_price'] = (temp['buy1'] * temp['bc1'] + temp['buy2'] * temp['bc2'] + temp['buy3'] * temp['bc3'] + temp['buy4'] * temp['bc4'] + temp['buy5'] * temp['bc5']) / temp['total_buy_vol']
    total_buy_vol = temp.total_buy_vol.tolist()
    VM_Avg_buy_price = temp.VM_Avg_buy_price.tolist()

    temp['total_sale_vol'] = temp['sc1'] + temp['sc2'] + temp['sc3'] + temp['sc4'] + temp['sc5']
    temp['VM_Avg_sale_price'] = (temp['sale1'] * temp['sc1'] + temp['sale2'] * temp['sc2'] + temp['sale3'] * temp['sc3'] + temp['sale4'] * temp['sc4'] + temp['sale5'] * temp['sc5']) / temp['total_sale_vol']
    VM_Avg_sale_price = temp.VM_Avg_sale_price.tolist()
    total_sale_vol = temp.total_sale_vol.tolist()

    # write data to the output csv file row by row
    sample_start = 0
    while sample_start + step + 10 + 10 < raw_data_length:
        row = raw_data_list[sample_start]
        # add the sixth and the seventh feature
        if math.isnan(VM_Avg_buy_price[sample_start]) or VM_Avg_buy_price[sample_start] > 300 or VM_Avg_buy_price[sample_start] < 1:
            if buy1[sample_start] + buy5[sample_start] == 0:
                row.insert(6, price[sample_start])
            else:
                row.insert(6, (buy1[sample_start] + buy5[sample_start]) / 2)
        else:
                row.insert(6, VM_Avg_buy_price[sample_start])

        if math.isnan(VM_Avg_sale_price[sample_start]) or VM_Avg_sale_price[sample_start] > 300 or VM_Avg_sale_price[sample_start] < 1:
            if sale1[sample_start] + sale5[sample_start] == 0:
                row.insert(7, price[sample_start])
            else:
                row.insert(7, (sale1[sample_start] + sale5[sample_start]) / 2)
        else:
            row.insert(7, VM_Avg_sale_price[sample_start])

        # add the aggressor side
        if sample_start == 0:
            row.insert(8, 0)
        else:
            # if price[sample_start] > price[sample_start - 1]:
            #     row.insert(8, 1)
            # elif price[sample_start] < price[sample_start - 1]:
            #     row.insert(8, -1)
            # else:
            #     row.insert(8, 0)
            row.insert(8, price[sample_start] - price[sample_start - 1])

        # add the relative_buy_vol and relative_sale_vol
        if sample_start < 40:
            row.insert(9, 1)
            row.insert(10, 1)
        else:
            temp1 = 0
            temp2 = 0
            for ind in range(sample_start - 40, sample_start):
                temp1 += total_buy_vol[ind]
                temp2 += total_sale_vol[ind]

            if temp1 < 1:
                row.insert(9, 1)
            else:
                if total_buy_vol[sample_start] / (temp1 / 40) > 5:
                    row.insert(9, 5)
                else:
                    row.insert(9, total_buy_vol[sample_start] / (temp1 / 40))

            if temp2 < 1:
                row.insert(10, 1)
            else:
                if total_sale_vol[sample_start] / (temp2 / 40) > 5:
                    row.insert(10, 5)
                else:
                    row.insert(10, total_sale_vol[sample_start] / (temp2 / 40))

        # add the VW_Avg_price and VW_Avg_price_delta
        temp = (VM_Avg_buy_price[sample_start] * total_buy_vol[sample_start] + VM_Avg_sale_price[sample_start] * total_sale_vol[sample_start]) / (total_buy_vol[sample_start] + total_sale_vol[sample_start])
        if math.isnan(temp) or temp > 300 or temp < 1:
            if buy5[sample_start] + sale5[sample_start] == 0:
                temp = price[sample_start]
            else:
                temp = (buy5[sample_start] + sale5[sample_start]) / 2
        row.insert(11, temp)
        row.insert(12, temp - price[sample_start])

        # add the label
        y_start = sample_start + step
        total_vol_30s = raw_data.vol[y_start + 10 - 10:y_start + 10 + 10].sum()
        vmap_30s = 0
        if total_vol_30s < 0.1:
            vmap_30s = raw_data.price[y_start + 10 - 10:y_start + 10 + 10].mean()
        else:
            for ind in range(-10, 10):
                vmap_30s += (vol[y_start + 10 + ind] / total_vol_30s) * price[y_start + 10 + ind]

        writer.writerow(row + [price[sample_start + 1], price[sample_start + 1] - price[sample_start], vmap_30s, (vmap_30s - price[sample_start]), mid_price[sample_start + 1] - mid_price[sample_start]])
        sample_start += step

    return


file_site = 'H:\Wechat\WeChat Files\hhufjdd\Files\AI&FintechLab 2018 Material\SH600031'
generate_csv2(file_site=file_site)
