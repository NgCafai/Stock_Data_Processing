import pandas as pd
import numpy as np
import csv
import os


class LabelGenerator:
    def __init__(self, raw_data):
        self.raw_data = raw_data

    def generate_label1(self, start_index, y_step):
        temp = self.raw_data.close[start_index:(start_index + y_step)].mean()
        return temp

    @staticmethod
    def generate_label2(file_site, stock_id, date_index, step, profit_taking, stop_loss, y_step):
        """
        If the upper barrier is touched first, we label the observation as a 1.
        If the lower barrier is touched first, we label the observation as a -1.
        Otherwise, we label the observation as a 0.
        :param file_site: the exact directory of the csv file
        :param step:
        :param profit_taking:
        :param stop_loss:
        :param y_step:
        :return:
        """
        # 读取该股票的所有文件列表
        file_list = os.listdir(file_site)

        f = open(file_site + '/' + file_list[date_index], 'r')
        raw_data = pd.read_csv(f)
        raw_data = raw_data[raw_data.close > 0]
        price = raw_data.close.tolist()
        raw_data_length = len(raw_data)

        csv_file = open('H:/sample_csv/' + stock_id + '/label_of_' + file_list[date_index], 'w', newline='')
        writer = csv.writer(csv_file)
        writer.writerow(['triple_barrier'])
        for y_start in range(step, raw_data_length - y_step + 1, step):
            if y_start + y_step <= raw_data_length:
                for ind in range(0, y_step):
                    if (price[y_start + ind] - price[y_start - 1]) / price[y_start - 1] > profit_taking:
                        writer.writerow([1])
                        break
                    elif (price[y_start + ind] - price[y_start - 1]) / price[y_start - 1] < -stop_loss:
                        writer.writerow([-1])
                        break

                    # when either upper or lower barrier is not touched, label the observation as a 0
                    if ind == y_step - 1:
                        writer.writerow([0])
        return





