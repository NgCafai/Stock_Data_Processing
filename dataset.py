import pandas as pd
import numpy as np
import os
from Feature import FeatureGenerator
from Label import LabelGenerator
import csv


class DataSetGenerator:
    @staticmethod
    def generate_data_set1(file_site, stock_id, start_date, end_date, n, step, look_back, y_step):
        """
            生成数据集, 数据集之间无交叉
            :param file_site: 文件位置，字符串类型，e.g."H:/SH600030"
            :param stock_id: 股票ID, 字符串类型，e.g."SH600030"
            :param start_date: 起始日期，int类型，e.g. 30（表示第三十个文件）
            :param stop_date: 结束日期，int类型
            :param n: 每一天取多少个sample，int类型
            :param step: 取多少条原始数据合成一组特征，int类型
            :param look_back: 取多少组特征合成一个sample的X，int类型
            :param y_step: 取多少条数据综合成一个label
            :return: X, list类型，其元素也是list类型
            :return: Y, list类型，其元素也是list类型
            :return: feature_length, int类型，单个bar内的特征数量
        """
        # 读取该股票的所有文件列表
        file_list = os.listdir(file_site)

        # 一个矩阵，每一行为一个sample的输入
        X = []

        # 一个向量，每个元素为一个sample的输出
        Y = []

        for ind in range(start_date, end_date):
            #读取某一天的具体数据
            f = open(file_site + '/' + file_list[ind], 'r')
            raw_data = pd.read_csv(f)
            raw_data = raw_data[raw_data.close > 0]
            raw_data_length = len(raw_data)

            fg = FeatureGenerator(raw_data, file_list, file_site, stock_id)
            lg = LabelGenerator(raw_data)
            sample_length = step * look_back + y_step    # 组建一条sample需要sample_length条原始数据
            for sample_start in range(1, 1 + 1 + (n - 1) * sample_length, sample_length):   #利用这一天的数据构建n个sample
                if sample_start + sample_length < raw_data_length:  # 确保下标没有超出raw_data的范围
                    sample_x = []     # 每个sample的输入
                    for bar_start in range(sample_start, 1 + sample_start + (look_back - 1) * step, step):
                        (bar_feature, feature_length) = fg.generate_x(bar_start, step)
                        sample_x = sample_x + bar_feature
                    sample_y = lg.generate_label1(sample_start, y_step)

                    X.append(sample_x)
                    Y.append(sample_y)
        return X,Y,feature_length

    @staticmethod
    def generate_data_set2(file_site, stock_id, start_date, end_date, n, step, look_back, y_step, time_difference):
        """
            生成数据集, 数据集之间有交叉
            :param file_site: 文件位置，字符串类型，e.g."H:/SH600030"
            :param stock_id: 股票ID, 字符串类型，e.g."SH600030"
            :param start_date: 起始日期，int类型，e.g. 30（表示第三十个文件）
            :param stop_date: 结束日期，int类型
            :param n: 每一天取多少个sample，int类型
            :param step: 取多少条原始数据合成一组特征，int类型
            :param look_back: 取多少组特征合成一个sample的X，int类型
            :param y_step: 取多少条数据综合成一个label
            :param time_difference: 前一条sample的起始点与当前数据的起始点差了多少条原始数据
            :return: X, list类型，其元素也是list类型
            :return: Y, list类型，其元素也是list类型
            :return: feature_length, int类型，单个bar内的特征数量
        """
        # 读取该股票的所有文件列表
        file_list = os.listdir(file_site)

        # 一个矩阵，每一行为一个sample的输入
        X = []

        # 一个向量，每个元素为一个sample的输出
        Y = []

        for ind in range(start_date, end_date):
            # 读取某一天的具体数据
            f = open(file_site + '/' + file_list[ind], 'r')
            raw_data = pd.read_csv(f)
            raw_data = raw_data[raw_data.close > 0]
            raw_data_length = len(raw_data)

            fg = FeatureGenerator(raw_data, file_list, file_site, stock_id)
            lg = LabelGenerator(raw_data)

            # 组建一条sample需要sample_length条原始数据
            sample_length = step * look_back + y_step

            # 利用这一天的数据构建n个sample
            sample_start = 1
            k = n
            while k > 0:
                if sample_start + sample_length < raw_data_length:  # 确保下标没有超出raw_data的范围
                    sample_x = []     # 每个sample的输入
                    for bar_start in range(sample_start, 1 + sample_start + (look_back - 1) * step, step):
                        (bar_feature, feature_length) = fg.generate_x(bar_start, step)
                        sample_x = sample_x + bar_feature
                    sample_y = lg.generate_label1(sample_start, y_step)

                    X.append(sample_x)
                    Y.append(sample_y)
                k -= 1
                sample_start += time_difference
        return X, Y, feature_length

    @staticmethod
    def generate_data_set3(file_site, stock_id, date_index, step):
        """
            生成数据集, 并写到csv文件
            :param file_site: 文件位置，字符串类型，e.g."H:/SH600030"
            :param stock_id: 股票ID, 字符串类型，e.g."SH600030"
            :param date_index: 需要处理的股票下标
            :param step: 取多少条原始数据合成一组特征，int类型
        """
        # 读取该股票的所有文件列表
        file_list = os.listdir(file_site)

        # 一个矩阵，每一行为一个sample的输入
        X = []

        # 一个向量，每个元素为一个sample的输出
        Y = []

        # 读取某一天的具体数据
        f = open(file_site + '/' + file_list[date_index], 'r')
        raw_data = pd.read_csv(f)
        raw_data = raw_data[raw_data.close > 0]
        raw_data_length = len(raw_data)

        fg = FeatureGenerator(raw_data, file_list, file_site, stock_id)
        # lg = LabelGenerator(raw_data)

        csv_file = open('H:/sample_csv/' + stock_id + '/feature_of_' + file_list[date_index], 'w', newline = '')
        writer = csv.writer(csv_file)
        for sample_start in range(0, raw_data_length - step, step):   #利用这一天的数据构建n个sample
            if sample_start + step < raw_data_length:  # 确保下标没有超出raw_data的范围
                (sample_feature, name_list, feature_length) = fg.generate_x(sample_start, step)
                if sample_start == 1:
                    writer.writerow(name_list)
                writer.writerow(sample_feature)

        return




