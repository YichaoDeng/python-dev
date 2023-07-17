import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

filepath = r'./files/'

fig = plt.figure(num='panel', figsize=(8, 4))

data = pd.read_csv(f'{filepath}/peptide_rmsd.csv')

data = data.dropna(axis=0)

headers_x = ['Time (ps)', 'Time (ps)', 'P3_Time', 'P4_Time', 'P5_Time']
headers_y = ['P1_RMSD', 'P2_RMSD', 'P3_RMSD', 'P4_RMSD', 'P5_RMSD']

# p1 = fig.add_subplot(5, 1, 1)
# p2 = fig.add_subplot(5, 1, 2)
# p3 = fig.add_subplot(5, 1, 3)
# p4 = fig.add_subplot(5, 1, 4)
# p5 = fig.add_subplot(5, 1, 5)

diffs = [0, 5, 10, 15, 20]

# plots = [p1, p2, p3, p4, p5]

colors = ['r', 'g', 'b', 'y', 'c']

p1 = fig.add_subplot(1, 1, 1)
p1.set_xlim(300000, 580000)

# for header_x, header_y, plot, color in zip(headers_x, headers_y, plots, colors):
#     x = data[header_x]
#     y = data[header_y]
#     plot.scatter(x, y, s=0.2)
#     parameter = np.polyfit(x, y, 17)
#     func = np.poly1d(parameter)
#     plot.plot(x, func(x), color=color)
#     plot.set_xlim(300000, 580000)

for header_x, header_y, color, diff in zip(headers_x, headers_y, colors, diffs):
    x = data[header_x]
    y = data[header_y] + diff

    # 先单独画散点
    p1.scatter(x, y, s=0.2, color='gray')
    # 计算拟合函数
    parameter = np.polyfit(x, y, 17)  # 可以设置 1-17， 越大坡度越抖
    func = np.poly1d(parameter)

    # 再画拟合曲线
    p1.plot(x, func(x), color=color)

fig.show()
