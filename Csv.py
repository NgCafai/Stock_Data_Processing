import pandas as pd
import numpy as np
import csv
import os


class CsvGenerator:
    @staticmethod
    def generate_csv1(file_site, stock_id, date_index, step=1):
        """
        If the upper barrier is touched first, we label the observation as a 1.
        If the lower barrier is touched first, we label the observation as a -1.
        Otherwise, we label the observation as a 0.
        :param file_site: the exact directory of the csv file, eg.'H:\Wechat\WeChat Files\hhufjdd\Files\AI&FintechLab 2018 Material\SH600637'
        :param stock_id:
        :param date_index:
        :param step:
        :return:
        """
        # 读取该股票的所有文件列表
        file_list = os.listdir(file_site)

        f = open(file_site + '/' + file_list[date_index], 'r')
        raw_data = pd.read_csv(f)
        # delete the useless data
        raw_data = raw_data[raw_data.close > 0]

        price = raw_data.close.tolist()
        vol = raw_data.vol.tolist()
        # transform raw_data to the type list
        raw_data_list = (np.array(raw_data)).tolist()

        raw_data_length = len(raw_data)

        # create the csv file in which we are going to write the data
        csv_file = open('H:/sample_csv/' + stock_id + '/feature_and_label_of_' + file_list[date_index], 'w', newline='')
        writer = csv.writer(csv_file)
        writer.writerow(raw_data.columns.values.tolist() + ['5min', '10min', '20min'])

        sample_start = 0
        while sample_start + step + 400 + 5 < raw_data_length:
            y_start = sample_start + step
            total_vol_5min = raw_data.vol[y_start + 100 - 5:y_start + 100 + 6].sum()
            total_vol_10min = raw_data.vol[y_start + 200 - 5:y_start + 200 + 6].sum()
            total_vol_20min = raw_data.vol[y_start + 400 - 5:y_start + 400 + 6].sum()
            vmap_5min = 0
            vmap_10min = 0
            vmap_20min = 0
            if total_vol_5min == 0:
                vmap_5min = raw_data.price[y_start + 100 - 5:y_start + 100 + 6].mean()
            else:
                for ind in range(-5, 6):
                    vmap_5min += (vol[y_start + 100 + ind] / total_vol_5min) * price[y_start + 100 + ind]

            if total_vol_10min == 0:
                vmap_10min = raw_data.price[y_start + 200 - 5:y_start + 200 + 6].mean()
            else:
                for ind in range(-5, 6):
                    vmap_10min += (vol[y_start + 200 + ind] / total_vol_10min) * price[y_start + 200 + ind]

            if total_vol_20min == 0:
                vmap_20min = raw_data.price[y_start + 400 - 5:y_start + 400 + 6].mean()
            else:
                for ind in range(-5, 6):
                    vmap_20min += (vol[y_start + 400 + ind] / total_vol_20min) * price[y_start + 400 + ind]

            writer.writerow(raw_data_list[sample_start] + [vmap_5min, vmap_10min, vmap_20min])
            sample_start += step
        return

    @staticmethod
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

        # delete the useless columns
        col_name = raw_data.columns.tolist()
        for ind in range(0, 5):
            raw_data.pop(col_name[ind])
        for ind in range(6, 10):
            raw_data.pop(col_name[ind])
        for ind in range(45, 60):
            raw_data.pop(col_name[ind])

        # add some features
        raw_data['mid_price'] = (raw_data['buy1'] + raw_data['sale1']) / 2
        mid_price = raw_data.pop('mid_price')
        raw_data.insert(1, 'mid_price', mid_price)

        col_name = raw_data.columns.tolist()
        col_name.insert(2, 'VM_Avg_buy_price')
        col_name.insert(3, 'VM_Avg_sale_price')
        col_name.insert(4, 'aggressor_side')
        col_name.insert(5, 'relative_buy_vol')
        col_name.insert(6, 'relative_sale_vol')
        # create the csv file in which we are going to write the data
        csv_file = open('H:\Wechat\WeChat Files\hhufjdd\Files\AI&FintechLab 2018 Material\Data\database_5days_1min.csv', 'w', newline='')
        writer = csv.writer(csv_file)
        writer.writerow(col_name + ['1min'])

        price = raw_data.close.tolist()
        vol = raw_data.vol.tolist()
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

        sample_start = 0
        while sample_start + step + 20 + 10 < raw_data_length:
            row = raw_data_list[sample_start]
            # add the third and the fourth feature
            row.insert(2, VM_Avg_buy_price[sample_start])
            row.insert(3, VM_Avg_sale_price[sample_start])

            if sample_start == 0:
                row.insert(4, 0)
            else:
                if price[sample_start] > price[sample_start - 1]:
                    row.insert(4, 1)
                elif price[sample_start] < price[sample_start - 1]:
                    row.insert(4, -1)
                else:
                    row.insert(4, 0)

            if sample_start < 20:
                row.insert(5, 1)
                row.insert(6, 1)
            else:
                temp1 = 0
                temp2 = 0
                for ind in range(sample_start - 20, sample_start):
                    temp1 += total_buy_vol[ind]
                    temp2 += total_sale_vol[ind]
                row.insert(5, total_buy_vol[sample_start] / (temp1 / 20))
                row.insert(6, total_sale_vol[sample_start] / (temp2 / 20))

            # add the label
            y_start = sample_start + step
            total_vol_1min = raw_data.vol[y_start + 20 - 10:y_start + 20 + 10].sum()
            vmap_1min = 0
            if total_vol_1min == 0:
                vmap_1min = raw_data.price[y_start + 20 - 10:y_start + 20 + 10].mean()
            else:
                for ind in range(-10, 10):
                    vmap_1min += (vol[y_start + 20 + ind] / total_vol_1min) * price[y_start + 20 + ind]

            writer.writerow(row + [vmap_1min])
            sample_start += step

        return





