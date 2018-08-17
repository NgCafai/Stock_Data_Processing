import pandas as pd
import numpy as np
import os


class FeatureGenerator:
    def __init__(self, raw_data, file_list, file_site, stock_id):
        self.raw_data = raw_data
        # 在原始数据对应的前五日的数据
        self.previous_5_days = 0
        self.time_list = raw_data.time.tolist()

        # raw_data的开始日期
        start_date = self.time_list[0][0:10]
        # 开始日期对应为文件在文件夹中的位置
        start_ind = file_list.index(stock_id + "_" + start_date +".csv")
        # 读取self.previous_5_days
        for ind in range(start_ind - 5, start_ind):
            f = open(file_site + '/' + file_list[ind], 'r')
            if type(self.previous_5_days) == int:
                self.previous_5_days = pd.read_csv(f)
            else:
                self.previous_5_days = self.previous_5_days.append(pd.read_csv(f))
            f.close()
        self.previous_5_days = self.previous_5_days[self.previous_5_days.close > 0]

    # 计算区间内的平均价格
    def __cal_price_mean(self, start_index, step):
        temp = self.raw_data.close[start_index:(start_index + step)].mean()
        return temp

    # 计算区间内价格的方差
    def __cal_price_std(self, start_index, step):
        temp = self.raw_data.close[start_index:(start_index + step)].std()
        return temp

    # 计算区间内价格的最大值
    def __cal_price_max(self, start_index, step):
        temp = self.raw_data.close[start_index:(start_index + step)].max()
        return temp

    # 计算区间内价格的最小值
    def __cal_price_min(self, start_index, step):
        temp = self.raw_data.close[start_index:(start_index + step)].min()
        return temp

    # 计算前五天价格的最大值
    def __cal_5_days_max(self):
        temp = self.previous_5_days.close[0:-1].max()
        return temp

    # 计算前五天价格的最小值
    def __cal_5_days_min(self):
        temp = self.previous_5_days.close[0:-1].min()
        return temp

    # 计算前五天价格的平均值
    def __cal_5_days_mean(self):
        temp = self.previous_5_days.close[0:-1].mean()
        return temp

    # 计算区间内成交量的总和
    def __cal_vol(self, start_index, step):
        temp = self.raw_data.vol[start_index:(start_index + step)].sum()
        return temp

    # 计算区间内成交金额的总和
    def __cal_amount(self, start_index, step):
        temp = self.raw_data.amount[start_index:(start_index + step)].sum()
        return temp

    # 计算区间内买一价格的平均值
    def __cal_buy1(self, start_index, step):
        temp = self.raw_data.buy1[start_index:(start_index + step)].mean()
        return temp

    # 计算区间内买三价格的平均值
    def __cal_buy3(self, start_index, step):
        temp = self.raw_data.buy3[start_index:(start_index + step)].mean()
        return temp

    # 计算区间内买五价格的平均值
    def __cal_buy5(self, start_index, step):
        temp = self.raw_data.buy5[start_index:(start_index + step)].mean()
        return temp

    # 计算区间内卖一价格的平均值
    def __cal_sale1(self, start_index, step):
        temp = self.raw_data.sale1[start_index:(start_index + step)].mean()
        return temp

    # 计算区间内卖三价格的平均值
    def __cal_sale3(self, start_index, step):
        temp = self.raw_data.sale3[start_index:(start_index + step)].mean()
        return temp

    # 计算区间内卖五价格的平均值
    def __cal_sale5(self, start_index, step):
        temp = self.raw_data.sale5[start_index:(start_index + step)].mean()
        return temp

    # 计算区间内买一数量的总和
    def __cal_bc1(self, start_index, step):
        temp = self.raw_data.bc1[start_index:(start_index + step)].sum()
        return temp

    # 计算区间内买三数量的总和
    def __cal_bc3(self, start_index, step):
        temp = self.raw_data.bc3[start_index:(start_index + step)].sum()
        return temp

    # 计算区间内卖一数量的总和
    def __cal_sc1(self, start_index, step):
        temp = self.raw_data.sc1[start_index:(start_index + step)].sum()
        return temp

    # 计算区间内卖三数量的总和
    def __cal_sc3(self, start_index, step):
        temp = self.raw_data.sc3[start_index:(start_index + step)].sum()
        return temp

    # 计算区间内委比的平均值
    def __cal_wb(self, start_index, step):
        temp = self.raw_data.wb[start_index:(start_index + step)].mean()
        return temp

    # 计算区间内量比的平均值
    def __cal_lb(self, start_index, step):
        temp = self.raw_data.lb[start_index:(start_index + step)].mean()
        return temp

    # 计算区间内委买量的总和
    def __cal_w_buy(self, start_index, step):
        temp = self.raw_data.w_buy[start_index:(start_index + step)].sum()
        return temp

    # 计算区间内委卖量的总和
    def __cal_w_sale(self, start_index, step):
        temp = self.raw_data.w_buy[start_index:(start_index + step)].sum()
        return temp

    # 区间内委买量/前五天平均委买量
    def __cal_relative_w_buy(self, start_index, step):
        average = self.previous_5_days.w_buy[0:-1].mean()
        average = average * step
        return self.__cal_w_buy(start_index, step) / average

    # 区间内委卖量/前五天平均委卖量
    def __cal_relative_w_sale(self, start_index, step):
        average = self.previous_5_days.w_sale[0:-1].mean()
        average = average * step
        return self.__cal_w_sale(start_index, step) / average

    # 计算开盘到当前时间的主买量之和
    def __cal_sectional_buy_vol(self, start_index, step):
        temp = self.raw_data.sectional_buy_vol[start_index:(start_index + step)].max()
        return temp

    # 计算开盘到当前时间的主买金额之和
    def __cal_sectional_buy_amount(self, start_index, step):
        temp = self.raw_data.sectional_buy_amount[start_index:(start_index + step)].max()
        return temp

    # 计算开盘到当前时间的主卖量之和
    def __cal_sectional_sale_vol(self, start_index, step):
        temp = self.raw_data.sectional_sale_vol[start_index:(start_index + step)].max()
        return temp

    # 计算开盘到当前时间的主卖金额之和
    def __cal_sectional_sale_amount(self, start_index, step):
        temp = self.raw_data.sectional_sale_amount[start_index:(start_index + step)].max()
        return temp

    # 计算开盘到当前时间的委买量之和
    def __cal_sectional_w_buy(self, start_index, step):
        temp = self.raw_data.sectional_w_buy[start_index:(start_index + step)].max()
        return temp

    # 计算开盘到当前时间的委卖量之和
    def __cal_sectional_w_sale(self, start_index, step):
        temp = self.raw_data.sectional_w_sale[start_index:(start_index + step)].max()
        return temp

    # 计算当日开盘价格
    def __cal_sectional_open(self, start_index, step):
        temp = self.raw_data.sectional_open[start_index:(start_index + step)].mean()
        return temp

    # 计算从开盘时间到当前时间的最高价
    def __cal_sectional_high(self, start_index, step):
        temp = self.raw_data.sectional_high[start_index:(start_index + step)].max()
        return temp

    # 计算从开盘时间到当前时间的最低价
    def __cal_sectional_low(self, start_index, step):
        temp = self.raw_data.sectional_low[start_index:(start_index + step)].min()
        return temp

    # 计算从开盘时间到当前时间的总成交量
    def __cal_sectional_vol(self, start_index, step):
        temp = self.raw_data.sectional_vol[start_index:(start_index + step)].max()
        return temp

    # 计算从开盘时间到当前时间的总成交金额
    def __cal_sectional_amount(self, start_index, step):
        temp = self.raw_data.sectional_amount[start_index:(start_index + step)].max()
        return temp


    # 对区间内的时点当日累计委比（当日累计委买/当日累计委卖）取平均值
    def __cal_sectional_wb(self, start_index, step):
        temp = self.raw_data.sectional_wb[start_index:(start_index + step)].mean()
        return temp

    # （区间内最后一条数据的时间 - 开盘时间）/ 4h
    def __cal_time(self, start_index, step):
        now = self.time_list[start_index + step - 1][11:19]
        hour = int(now[0:2])
        min = int(now[3:5])
        if hour <= 11:
            hour_difference = hour - 9
        else:
            hour_difference = hour - 1.5 - 9

        time_difference = hour_difference * 60.00 + min - 30
        return time_difference / 240

    def generate_x(self, start_index, step):
        feature_list = []
        name_list = []
        total_feature = 0
        feature_list.append(self.__cal_price_mean(start_index, step))
        name_list.append('price_mean')
        total_feature += 1
        feature_list.append(self.__cal_price_std(start_index, step))
        name_list.append('price_std')
        total_feature += 1
        feature_list.append(self.__cal_price_max(start_index, step))
        name_list.append('price_max')
        total_feature += 1
        feature_list.append(self.__cal_price_min(start_index, step))
        name_list.append('price_min')
        total_feature += 1
        feature_list.append(self.__cal_5_days_max())
        name_list.append('five_days_max')
        total_feature += 1
        feature_list.append(self.__cal_5_days_min())
        name_list.append('five_days_min')
        total_feature += 1
        feature_list.append(self.__cal_5_days_mean())
        name_list.append('five_days_mean')
        total_feature += 1
        feature_list.append(self.__cal_vol(start_index, step))
        name_list.append('vol')
        total_feature += 1
        feature_list.append(self.__cal_amount(start_index, step))
        name_list.append('amount')
        total_feature += 1
        feature_list.append(self.__cal_buy1(start_index, step))
        name_list.append('buy1')
        total_feature += 1
        feature_list.append(self.__cal_buy3(start_index, step))
        name_list.append('buy3')
        total_feature += 1
        feature_list.append(self.__cal_buy5(start_index, step))
        name_list.append('buy5')
        total_feature += 1
        feature_list.append(self.__cal_sale1(start_index, step))
        name_list.append('sale1')
        total_feature += 1
        feature_list.append(self.__cal_sale3(start_index, step))
        name_list.append('sale3')
        total_feature += 1
        feature_list.append(self.__cal_sale5(start_index, step))
        name_list.append('sale5')
        total_feature += 1
        feature_list.append(self.__cal_bc1(start_index, step))
        name_list.append('bc1')
        total_feature += 1
        feature_list.append(self.__cal_bc3(start_index, step))
        name_list.append('bc3')
        total_feature += 1
        feature_list.append(self.__cal_sc1(start_index, step))
        name_list.append('sc1')
        total_feature += 1
        feature_list.append(self.__cal_sc3(start_index, step))
        name_list.append('sc3')
        total_feature += 1
        feature_list.append(self.__cal_wb(start_index, step))
        name_list.append('wb')
        total_feature += 1
        feature_list.append(self.__cal_lb(start_index, step))
        name_list.append('lb')
        total_feature += 1
        feature_list.append(self.__cal_w_buy(start_index, step))
        name_list.append('w_buy')
        total_feature += 1
        feature_list.append(self.__cal_w_sale(start_index, step))
        name_list.append('w_sale')
        total_feature += 1
        feature_list.append(self.__cal_relative_w_buy(start_index, step))
        name_list.append('relative_w_buy')
        total_feature += 1
        feature_list.append(self.__cal_relative_w_sale(start_index, step))
        name_list.append('relative_w_sale')
        total_feature += 1
        feature_list.append(self.__cal_sectional_buy_vol(start_index, step))
        name_list.append('sectional_buy_vol')
        total_feature += 1
        feature_list.append(self.__cal_sectional_buy_amount(start_index, step))
        name_list.append('sectional_buy_amount')
        total_feature += 1
        feature_list.append(self.__cal_sectional_sale_vol(start_index, step))
        name_list.append('sectional_sale_vol')
        total_feature += 1
        feature_list.append(self.__cal_sectional_sale_amount(start_index, step))
        name_list.append('sectional_sale_amount')
        total_feature += 1
        feature_list.append(self.__cal_sectional_w_buy(start_index, step))
        name_list.append('sectional_w_buy')
        total_feature += 1
        feature_list.append(self.__cal_sectional_w_sale(start_index, step))
        name_list.append('sectional_w_sale')
        total_feature += 1
        feature_list.append(self.__cal_sectional_open(start_index, step))
        name_list.append('sectional_open')
        total_feature += 1
        feature_list.append(self.__cal_sectional_high(start_index, step))
        name_list.append('sectional_high')
        total_feature += 1
        feature_list.append(self.__cal_sectional_low(start_index, step))
        name_list.append('sectional_low')
        total_feature += 1
        feature_list.append(self.__cal_sectional_vol(start_index, step))
        name_list.append('sectional_vol')
        total_feature += 1
        feature_list.append(self.__cal_sectional_amount(start_index, step))
        name_list.append('sectional_amount')
        total_feature += 1
        feature_list.append(self.__cal_sectional_wb(start_index, step))
        name_list.append('sectional_wb')
        total_feature += 1
        feature_list.append(self.__cal_time(start_index, step))
        name_list.append('time')
        total_feature += 1
        return feature_list, name_list, total_feature

