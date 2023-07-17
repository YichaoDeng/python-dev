import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Source Code Pro for Powerline'
plt.rcParams['font.sans-serif'] = ['Arial']

df_1 = pd.read_csv('./files/real.csv', sep=' ')
known_x = df_1.iloc[:, 0]
known_y = df_1.iloc[:, 1]
known_curve = np.column_stack((known_x, known_y))

df_2 = pd.read_csv('./files/siml.csv', sep=' ')
unknown_x1 = df_2.iloc[:, 0]
unknown_x2 = df_2.iloc[:, 1]
unknown_x3 = df_2.iloc[:, 2]

unknown_y = 0.3 * unknown_x1 + 0.3 * unknown_x2 + 0.4 * unknown_x3
unknown_curve = np.column_stack((known_x, unknown_y))

# 使用最小二乘法计算回归系数
X = np.column_stack((unknown_x1, unknown_x2, unknown_x3, np.ones(len(unknown_x1))))
beta = np.linalg.inv(X.T @ X) @ X.T @ unknown_y

predicted_y = X @ beta

SS_res = np.sum((unknown_y - predicted_y) ** 2)
SS_tot = np.sum((unknown_y - np.mean(unknown_y)) ** 2)
R2 = 1 - SS_res / SS_tot

# 输出回归系数和R方值
print(f'a = {beta[0]}, b = {beta[1]}, c = {beta[2]}, R2 = {R2}')

# 绘制已知曲线和拟合曲线的图像
plt.plot(known_x, known_y, label='known')
plt.plot(known_x, unknown_y, label='unknown')
plt.plot(known_x, predicted_y, label='predicted')
plt.legend()
plt.show()