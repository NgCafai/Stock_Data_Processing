import numpy as np
import pandas as pd
from scipy.stats import pearsonr
from scipy.stats import kstest


# x = [1, 2, 3]
# y = [1, 2, 3]
# print(pearsonr(x, y))

f = open('H:\Wechat\WeChat Files\hhufjdd\Files\AI&FintechLab 2018 Material\Data\database_SH600031.csv', 'r')
data = pd.read_csv(f)
f.close()

aggressor_side = data.aggressor_side.tolist()
relative_buy_vol = data.relative_buy_vol.tolist()
wb = data.wb.tolist()

half_minute_delta = data['30s_delta'].tolist()
next_delta = data.next_delta.tolist()

# test for wb
wb_next_delta = []
for i in range(0, len(wb)):
    if (wb[i] - 1) * next_delta[i] > 0:
        wb_next_delta.append(1)
    elif (wb[i] - 1) * next_delta[i] < 0:
        wb_next_delta.append(0)

sum = 0
for i in range(0, len(wb_next_delta)):
    sum += wb_next_delta[i]
print(sum / float(len(wb_next_delta)))

wb_delta = [0]
for i in range(1, len(wb)):
    wb_delta.append(wb[i] - wb[i - 1])
pearsonr(wb_delta, next_delta)

# test for aggressor side
aggressor_side_int = []
for i in range(0, len(aggressor_side)):
    if aggressor_side[i] > 0:
        aggressor_side_int.append(1)
    elif aggressor_side[i] < 0:
        aggressor_side_int.append(-1)
    else:
        aggressor_side_int.append(0)



